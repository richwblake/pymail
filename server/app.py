from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import dotenv_values
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import re
import ipdb

from models import db, Receiver, Message, MessageField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app, resources={r'/*': {'origins': [
    'https://statesoleil.com', 
    'https://www.statesoleil.com', 
    'https://willsblake.tech', 
    'https://www.willsblake.tech']}})
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['POST'])
def messages():
    if request.method == 'POST':

        # Get receiver base on request origin
        origin = request.headers.get('origin')

        match = re.search(r'www', origin)

        if not match:
            origin = origin[:8] + 'www.' + origin[8:]

        receiver = Receiver.query.filter_by(origin=origin).first()

        if not receiver:
            return make_response({ 'message': f'Request unauthorized, bad origin: {origin}' }, 401)
        else:
            new_message = build_message(request.get_json())
            receiver.messages.append(new_message)

            db.session.add(receiver)
            db.session.commit()

            send_message(new_message)

            return make_response(new_message.to_dict(), 201)

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

    # Configure smtp credentials 
    smtp_server = 'smtp.gmail.com'
    smtp_port = '587'
    smtp_username = env['SENDER_USER']
    smtp_password = env['SENDER_PASS']
    receiver = message.receiver.email 

    # build email message
    msg = build_email_from_message(message, smtp_username)

    # Send email via SMTP
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, message.receiver.email, text)

def build_email_from_message(message, smtp_sender):
    # e-mail metadata 
    subject = f'Inquiry from {message.receiver.origin}'

    # form data converted to string for e-mail body
    body_intro = f'Hi {message.receiver.name},\n\nYou\'ve received a new inquiry. Please see the rest of the message for more details.'
    formatted_formdata = body_intro + '\n\n'+ '~~~MESSAGE START~~~\n\n' + '\n\n'.join(f'{field.title.upper()}: {field.content}' for field in message.message_fields)

    # Create message object
    msg = MIMEMultipart()
    msg['From'] = smtp_sender
    msg['To'] = message.receiver.email
    msg['Subject'] = subject
    msg.attach(MIMEText(formatted_formdata, 'plain'))

    return msg

if __name__ == '__main__':
    app.run(port=5555, debug=True)
