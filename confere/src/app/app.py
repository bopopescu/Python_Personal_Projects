from flask import Flask
from flask_restful import Api
from db import db
from resources.loja_resource import Loja
from resources.funcao_resource import Funcao


# Map flask to the app
app = Flask(__name__)

# Map flask to the restful resources
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://app_purge:Senh%401ndefinid4@192.168.33.20/sistema_confere'
app.config['SQLALCHEMY_ECHO'] = True

# For this to execute is 
@app.before_first_request
def create_tables():
	print("It's happening!")
	db.create_all()

api.add_resource(Loja,'/loja/<int:_id>', '/loja')
api.add_resource(Funcao,'/funcao/<int:_id>', '/funcao')


if __name__ == '__main__':
	from db import db
	db.init_app(app)

	app.run(port=5000,debug=True)