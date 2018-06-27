# Importing the Flask class from the flask libraries
# jsonify takes a dictionary and transforms it into a json
# request function 
from flask import Flask, jsonify, request, render_template;		

# __name__ especial Python variable, gives each file a unique name
app = Flask(__name__)			

# In memory data
stores = [
	{
		'name':'My Wonderful Store',
		'items': [
			{'name': 'My Item', 'price': 15.99}
		]
	}
]

# Using a decorator to respond to the home of the application, this identify the location of he URL
@app.route('/')						
def home():
	# Calls by default the index.html file inside the templates folder
	return render_template('index.html')

# method argument chooses which http method we use to trigger this method
@app.route('/store', methods=['POST'])
def create_store():
	request_data = request.get_json()
	new_store = {
		'name': request_data['name'],
		'items': []
	}
	stores.append(new_store)
	return jsonify(new_store)


# <type:paramenter> is a especial Flask syntax to receive resources variables
@app.route('/store/<string:name>')	
def get_store(name):

	for store in stores:
		if store['name'] == name:
			return jsonify(store)

	return jsonify({'message': 'Store :{} not found'.format(name)})


@app.route('/store')
def get_stores():
	# jsonify only receives a dictionary as agument, so we transform the list into a dictionary
	return jsonify({'stores': stores})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
	
	request_data = request.get_json()

	for store in stores:
		if store['name'] == name:
			
			new_item = {
				'name' : request_data['name'],
				'price': request_data['price']
			}
			
			store['items'].append(new_item)

			return jsonify(new_item)
	
	return jsonify({'message': 'store not found'})


@app.route('/store/<string:name>/item')
def get_item_in_store(name):
	for store in stores:
		if store['name'] == name:
			return jsonify({'items': store['items']})

	return jsonify({'message': 'Not found'}) 


@app.route('/store/<string:name>/item')
def get_items_in_store(name):
	
	for store in stores:
		if store['name'] == name:
			return jsonify(store['items'])

	return jsonify({'message': 'Store item not found'})

# Runs the app deciding in which port which will receive the requests, it goes from 1 to 65535
app.run(port=5000)				