from flask import Flask, render_template, redirect, url_for
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore, current_user, roles_accepted
from endpoints import pedido_endpoint, admin_endpoint, loja_endpoint, pedido_servico_endpoint
import persistence as mysql_persistence
from app_util.flask_util import FlaskUtilJs
from app_util import format_datetime
from model import User, Role
from endpoints.forms import CustomizedChangePasswordForm
from sqlalchemy import text
# import endpoints.pedido_endpoint as pedido_endpoint
# import endpoints.loja_endpoint as loja_endpoint
# from app_util.flask_util import FlaskUtilJs

# Create a config file to specify how it will run based on the cfg file
# Set the FLASK_ENV enviroment variable
# export FLASK_ENV=development


# this will change
LOCAL_PATH = '/home/vyosiura/config-files/'
# LOCAL_PATH = '/home/vinicius/config-files/'

app = Flask(__name__, instance_path=LOCAL_PATH)
fujs = FlaskUtilJs(app)
app.config.from_pyfile(app.instance_path + 'flask.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'] % (
    app.config['SQL_USER'], app.config['SQL_PASSWORD'])

mysql_persistence.db.init_app(app)

user_datastore = SQLAlchemySessionUserDatastore(mysql_persistence.db.session, User, Role)

security = Security(app, user_datastore, 
	change_password_form=CustomizedChangePasswordForm)
app.register_blueprint(admin_endpoint.bp)
app.register_blueprint(pedido_endpoint.bp)
app.register_blueprint(loja_endpoint.bp)
app.register_blueprint(pedido_servico_endpoint.bp)

app.jinja_env.filters['datetime_pretty'] = format_datetime

@app.route("/")
@login_required
def index():

	if current_user.roles[0].name == 'admin':
		return redirect(url_for('admin.index'))
	elif current_user.roles[0].name == 'medidor': # See only 
		return redirect(url_for('pedido.medicao'))
	elif current_user.roles[0].name == 'projetista': # See only the pedido_servico which are 'Liberacao', 'Subir Paredes' e 'Projetos'
		return redirect(url_for('pedido.projetista'))
	elif current_user.roles[0].name == 'controladora':
		return redirect(url_for('pedido.pedidos'))

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
