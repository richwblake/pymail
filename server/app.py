from flask import Flask, request, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from pprint import pprint
import ipdb

from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/meta')
def meta():
    pprint(dict(request.headers))
    return make_response({'message': 'request okay, metadata logged'}, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
