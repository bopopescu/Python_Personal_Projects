import json

def dict_to_str(dic):
	return json.dumps(dic)

def str_to_dic(json_str):
	return json.loads(json_str)
