from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import dotenv_values
import ipdb

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
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

        send_message(message.content)

        return make_response(message.to_dict(), 201)


def send_message(message):
    env = dotenv_values('.env')

    
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
