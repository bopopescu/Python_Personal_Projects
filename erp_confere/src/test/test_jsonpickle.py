import jsonpickle
import decimal

class Another(object):

	def __init__(self, another_name, another_lis):
		self.another_name = another_name
		self.another_lis = another_lis


class Thing(object):

	def __init__(self, name, numer, lis, another):
		self.name = name
		self.numer = numer
		self.lis = lis
		self.another = another


# Creating a handler class to serialize and deserialize. 
class DecimalHandler(jsonpickle.handlers.BaseHandler):

	def flatten(self, obj, data):

		return float(obj)

# class ListHandler(jsonpickle.handlers.BaseHandler):

# 	def flatten(self, obj, data):

# 		print(obj)
# 		print(data)
# 		return data

# class ThingHandler(jsonpickle.handlers.BaseHandler):

# 	def flatten(self, obj, data):

# 		print(obj.name)
# 		print(data)

# 		data['name'] = obj.name
# 		data['numer'] = float(obj.numer)
# 		data['lis'] = obj.lis
# 		print(type(obj.lis))
# 		return data

# Register the Handler class to the specific class 
jsonpickle.handlers.register(decimal.Decimal, DecimalHandler)
# jsonpickle.handlers.register(list, ListHandler)
# jsonpickle.handlers.register(Thing, ThingHandler)


obj = Thing('Awesome', decimal.Decimal(10.24), [10, 20, 30], Another('nome', ['o', 's']))

str_json_obj = jsonpickle.encode(obj, unpicklable=False)

print(str_json_obj)


# If unpicklable=False was used to encode the object, then the necessary information
# Won't be there to decode the object
# json_str_to_obj = jsonpickle.decode(str_json_obj)	# Transoforms the string into a object

# print(json_str_to_obj.name)
