from flask import Flask, render_template
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy
from endpoints import pedido_endpoint
import persistence.mysql_persistence as mysql_persistence
# import endpoints.pedido_endpoint as pedido_endpoint
# import endpoints.loja_endpoint as loja_endpoint
# from app_util.flask_util import FlaskUtilJs

# Create a config file to specify how it will run based on the cfg file 
# Set the FLASK_ENV enviroment variable 
	# export FLASK_ENV=development

# this will change
LOCAL_PATH = '/home/vyosiura/config-files/'

app = Flask(__name__, instance_path=LOCAL_PATH)
app.config.from_pyfile(app.instance_path+'flask.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'] % (app.config['SQL_USER'], app.config['SQL_PASSWORD'])
mysql_persistence.db.init_app(app)

app.register_blueprint(pedido_endpoint.bp)

@app.route("/")
def template_test():
	return render_template('index.html', my_string="Wheeee!", my_list=[0,1,2,3,4,5])


# app.register_blueprint(loja_endpoint.loja)

if __name__ == '__main__':

	# from services.ambiente_service import get_all_ambientes
	# from services.loja_service import query_all_lojas, query_loja_by_id
	# from services.servico_service import query_all_servicos, query_servico_by_id
	# from services.cep_service import cep_handler, query_cep_by_id

	# print(query_cep_by_id('04256090'))

	app.run(threaded=True)
