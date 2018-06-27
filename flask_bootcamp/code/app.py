from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
# Exposed the app to the API class
api = Api(app)

# All classes which are going to be exposed as a resource must extend Resource class
class Student(Resource):


	def get(self,name):
		return { 'student': name }


# Makes the resource accessable 
api.add_resource(Student, '/student/<string:name>') # http://localhost:5000/student/Rolf


# Run the app listening at port 5000
app.run(port=5000)