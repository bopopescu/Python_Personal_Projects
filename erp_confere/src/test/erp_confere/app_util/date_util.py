import datetime

def convert_form_date_to_date(form_date):

	values = form_date.split('/')
	day = int(values[0])
	month = int(values[1])
	year = int(values[2])

	return datetime.date(year, month, day)