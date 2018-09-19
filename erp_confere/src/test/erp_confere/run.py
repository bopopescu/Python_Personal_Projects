from flask import Flask, render_template, redirect, url_for
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore, current_user, roles_accepted
from endpoints import pedido_endpoint
import persistence.mysql_persistence as mysql_persistence
from app_util.flask_util import FlaskUtilJs
from model.models import User, Role
# import endpoints.pedido_endpoint as pedido_endpoint
# import endpoints.loja_endpoint as loja_endpoint
# from app_util.flask_util import FlaskUtilJs

# Create a config file to specify how it will run based on the cfg file
# Set the FLASK_ENV enviroment variable
# export FLASK_ENV=development


# this will change
# LOCAL_PATH = '/home/vyosiura/config-files/'
LOCAL_PATH = '/home/vinicius/config-files/'

app = Flask(__name__, instance_path=LOCAL_PATH)
fujs = FlaskUtilJs(app)
app.config.from_pyfile(app.instance_path + 'flask.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'] % (
    app.config['SQL_USER'], app.config['SQL_PASSWORD'])

mysql_persistence.db.init_app(app)

user_datastore = SQLAlchemySessionUserDatastore(mysql_persistence.db.session, User, Role)

security = Security(app, user_datastore)
app.register_blueprint(pedido_endpoint.bp)



@app.route("/")
@login_required
def template_test():
	for role in current_user.roles:
		print(role.name)
	if current_user.roles[0].name == 'admin':
		return render_template('admin/index.html', my_string="Wheeee!", my_list=[0, 1, 2, 3, 4, 5])
	elif current_user.roles[0].name == 'medidor': # See only 
		return redirect(url_for('pedido.medicao'))
	elif current_user.roles[0].name == 'projetista': # See only the pedido_servico which are 'Liberacao', 'Subir Paredes' e 'Projetos'
		pass 

@app.errorhandler(403)
def forbidden(e):
	return render_template('403.html'), 403

# app.register_blueprint(loja_endpoint.loja)

if __name__ == '__main__':

    # from services.ambiente_service import get_all_ambientes
    # from services.loja_service import query_all_lojas, query_loja_by_id
    # from services.servico_service import query_all_servicos, query_servico_by_id
    # from services.cep_service import cep_handler, query_cep_by_id

    # print(query_cep_by_id('04256090'))

    app.run(threaded=True)
