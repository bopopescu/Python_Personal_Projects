import unidecode
import re
import string
import random
import decimal
from wtforms import DecimalField

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


# Creating a custom decimal field to handle the Decimal field with comma
class CustomDecimalField(DecimalField):

	def __init__(self, label='', validators=None, remove_duplicates=True, **kwargs):
		super(CustomDecimalField, self).__init__(label, validators, **kwargs)

	def process_formdata(self, valuelist):

		if valuelist:
			is_pattern_ok = re.compile('^[0-9]+(,|.)[0-9]*$')
			if is_pattern_ok:
				if valuelist[0]: 
					valuelist[0] = valuelist[0].replace(',', '.')

				try:
					if self.use_locale:
						self.data = self._parse_decimal(valuelist[0])
					else:
						self.data = decimal.Decimal(valuelist[0])
				except (decimal.InvalidOperation, ValueError):
					self.data = None
					raise ValueError(self.gettext("Valor incorreto no campo Decimal, favor verificar"))


