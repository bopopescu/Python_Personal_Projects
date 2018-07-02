from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from security import authenticate, identity

app = Flask(__name__)

# This key should be secret, encrypt it or something like that
app.secret_key = 'vinicius'

# Exposed the app to the API class
api = Api(app)

# Flask sqlalchemy disabled so it doesn't overwirte anythin form SQLAlchemy itself
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Creates a new endpoint /auth
# Sends in the body username and password to pass to authenticate function
# The /auth endpoint returns a token if there is a match
# We use it to make every request we make 
# the identity authenticate the token sended by the request and validates it 
jwt = JWT(app, authenticate, identity) 

@app.before_first_request
def create_tables():
	db.create_all()

# Makes the resource accessable 
api.add_resource(Item, '/item/<string:name>') # http://localhost:5000/student/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
	from db import db
	db.init_app(app)
	# Run the app listening at port 5000
	# Don't use debug on production environments
	app.run(port=5000, debug=True)