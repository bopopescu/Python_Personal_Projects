import unidecode
import re
import string
import random

def create_system_user(nome, sobrenome):
	name = nome.strip().split(' ')[0]
	name = re.sub('[^A-Za-z]+', '',unidecode.unidecode(name.strip().lower()))
	last_name = sobrenome.strip().split(' ')[-1]
	last_name = re.sub('[^A-Za-z]+', '',unidecode.unidecode(last_name.strip().lower())) 
	return name+'.'+last_name


def password_generator(size=9, chars=string.ascii_letters + string.digits):
	"""
	Returns a string of random characters, useful in generating temporary
	passwords for automated password resets.

	size: default=8; override to provide smaller/larger passwords
	chars: default=A-Za-z0-9; override to provide more/less diversity

	Credit: Ignacio Vasquez-Abrams
	Source: http://stackoverflow.com/a/2257449
	"""
	return ''.join(random.choice(chars) for i in range(size))


