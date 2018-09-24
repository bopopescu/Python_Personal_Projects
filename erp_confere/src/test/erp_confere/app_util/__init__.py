import unidecode
import re

def create_system_user(nome, sobrenome):
	name = nome.strip().split(' ')[0]
	name = re.sub('[^A-Za-z]+', '',unidecode.unidecode(name.strip().lower()))
	last_name = sobrenome.strip().split(' ')[-1]
	last_name = re.sub('[^A-Za-z]+', '',unidecode.unidecode(last_name.strip().lower())) 
	return name+'.'+last_name




