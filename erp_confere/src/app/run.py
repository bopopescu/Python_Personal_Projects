from flask import Flask, render_template
import endpoints.pedido_endpoint as pedido_endpoint
import endpoints.loja_endpoint as loja_endpoint


app = Flask(__name__)

app.secret_key = '123'

@app.route("/")
def template_test():
	return render_template('index.html', my_string="Wheeee!", my_list=[0,1,2,3,4,5])

app.register_blueprint(pedido_endpoint.bp)
app.register_blueprint(loja_endpoint.loja)

if __name__ == '__main__':

	app.run(debug=True)