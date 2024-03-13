from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import dotenv_values
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ipdb

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app, resources={r'/*': {'origins': ['https://willsblake.tech', 'https://www.willsblake.tech']}})
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['POST'])
def messages():
    if request.method == 'POST':
        message = Message()

        for attr in request.get_json():
            setattr(message, attr, request.get_json()[attr])


        db.session.add(message)
        db.session.commit()

        # TODO: BRING BACK IN TO TEST MAILING 
        # send_message(message)

        return make_response(message.to_dict(), 201)


def send_message(message):
    env = dotenv_values('.env')

    # e-mail content details
    subject = f'Pymail from {message.name} (willsblake.tech)'
    body = f'RETURN ADDRESS: {message.email}\n\nMESSAGE BODY: {message.content}'

    # Configure smtp credentials 
    smtp_server = 'smtp.gmail.com'
    smtp_port = '587'
    smtp_username = env['SENDER_USER']
    smtp_password = env['SENDER_PASS']
    receiver = env['RECEIVER']
    
    # Create message object
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email via SMTP

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, receiver, text)

    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
