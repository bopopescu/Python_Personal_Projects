import flask from Flask


Flask(__name__) # Object to create the initialize the app, __name__ especial variable as an arguement  

@app.route('/', methods=['GET', 'POST', 'PUT', 'DEL'])	# Decorator for a resource function. the uri and methods are the parameters
# FLASK RESTFUL
# http://flask-restful.readthedocs.io/en/0.3.5/quickstart.html
# A more productive way of developing a REST api using flask building block and taking into a next level
# Relies basically on Resource and Api objects