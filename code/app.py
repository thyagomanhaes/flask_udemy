from flask import Flask
from flask.json import jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.secret_key = "jose"

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# app.config['JWT_AUTH_URL_RULE'] = '/login' # If we want to change the url authentication endpoint, for instance,
# we want to use /login instead of /auth
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)


@jwt.auth_response_handler
def customized_response_handler(access_token, _identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': _identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
