from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import dotenv_values
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ipdb

from models import db, Receiver, Message, MessageField

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

        # Get receiver base on request origin
        origin = request.headers.get('origin')
        receiver = Receiver.query.filter_by(origin=origin).first()
        
        if not receiver:
            return make_response({ 'message': f'Request unauthorized, bad origin: {origin}' }, 401)
        else:
            new_message = build_message(request.get_json())
            receiver.messages.append(new_message)

            db.session.add(receiver)
            db.session.commit()

            return make_response(new_message.to_dict(), 201)



        # TODO: BRING BACK IN TO TEST MAILING 
        # send_message(message)


def build_message(form_data):
    return build_message_fields(Message(), form_data)

def build_message_fields(message, form_data):
    for attr, val in form_data.items():
        new_field = MessageField()
        new_field.title = attr
        new_field.content = val
        message.message_fields.append(new_field)

    return message


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
