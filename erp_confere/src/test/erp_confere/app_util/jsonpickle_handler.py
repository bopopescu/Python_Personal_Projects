import jsonpickle
import decimal
import datetime

class DecimalHandler(jsonpickle.handlers.BaseHandler):

	def flatten(self,obj,data):
		return float(obj)


jsonpickle.handlers.register(decimal.Decimal, DecimalHandler)