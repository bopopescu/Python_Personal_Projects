from flask import Flask, render_template
import endpoints.pedido_endpoint as pedido_endpoint
import endpoints.loja_endpoint as loja_endpoint
from app_util.flask_util import FlaskUtilJs


# Create a config file to specify how it will run based on the cfg file 
# Set the FLASK_ENV enviroment variable 
	# export FLASK_ENV=development



app = Flask(__name__, instance_path='/home/config-files')
fujs = FlaskUtilJs(app)

print(app.secret_key)

@app.route("/")
def template_test():
	return render_template('index.html', my_string="Wheeee!", my_list=[0,1,2,3,4,5])

# app.register_blueprint(pedido_endpoint.bp)
# app.register_blueprint(loja_endpoint.loja)

if __name__ == '__main__':

	app.run()