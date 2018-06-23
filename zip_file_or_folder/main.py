import datetime
import argparse
import os 
import sys
import pathlib 
import platform
from zipfile import ZipFile, ZIP_DEFLATED

def creation_date(filename):
	
	if platform.system() == 'Windows':
		last_modified_date = os.path.getctime(filename)
	else:
		status_info = os.stat(filename)
		last_modified_date = status_info.st_ctime

	return datetime.datetime.fromtimestamp(last_modified_date).date()


def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def valid_date(date_as_str):
	try:
		return datetime.datetime.strptime(date_as_str, '%Y-%m-%d').date()
	except ValueError:
		msg = 'Not a valid date: {}. The date should be in this format: YYYY-MM-DD'.format(date_as_str)
		argparse.ArgumentTypeError(msg)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Compress files with the same date into a single .zip file')

	parser.add_argument('pathname', help='The directory of the files')
	parser.add_argument('name', help='Name of the zip file')
	parser.add_argument('-d', '--date', help='date of the files that will be zipped all together in one file', type=valid_date)
	parser.add_argument('-v', '--validate', help='Validate zip file created', action='store_true')

	args = parser.parse_args()

	print(args.date)
	print(args.name)

	directory = pathlib.Path(args.pathname)
	os.chdir(args.pathname)

	# Separa só o que for arquivo
	files_to_zip = [content for content in directory.iterdir() if content.is_file()]
	
	# Separa só o que for da data passada
	files_to_zip = [content for content in files_to_zip if creation_date(content) == args.date]

	zip_file_name = args.name + '.zip'

	with ZipFile(zip_file_name, 'w', ZIP_DEFLATED) as zip_destination_file:

		for files in files_to_zip:
			zip_destination_file.write(files, os.path.basename(files))

		if args.validate:
			is_file_ok = zip_destination_file.testzip()

			if is_file_ok is None: 
				print('File created successfully and validated')
				
		else:
			print('File created successfully')
