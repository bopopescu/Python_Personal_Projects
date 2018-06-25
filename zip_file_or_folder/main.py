import datetime
import argparse
import os 
import sys
import pathlib 
import platform
from zipfile import ZipFile, ZIP_DEFLATED

def creation_date(filename):
	
	if platform.system() == 'Windows':
		last_modified_date = os.path.getmtime(filename)
	else:
		status_info = os.stat(filename)
		last_modified_date = status_info.st_mtime

	return datetime.datetime.fromtimestamp(last_modified_date).date()


def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)


def set_date_for_files(files):
	
	current_date = datetime.datetime.today().date()
	
	is_date_ok = True
	while is_date_ok:
		print(current_date)
		for file in files:
			if current_date == creation_date(file):
				is_date_ok = False
				break;

		if is_date_ok:
			current_date = current_date + datetime.timedelta(days=-1);
			print(current_date)

	return current_date


# def valid_date(date_as_str):
# 	try:
# 		return datetime.datetime.strptime(date_as_str, '%Y-%m-%d').date()
# 	except ValueError:
# 		msg = 'Not a valid date: {}. The date should be in this format: YYYY-MM-DD'.format(date_as_str)
# 		argparse.ArgumentTypeError(msg)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Compress files with the same date into a single .zip file')

	parser.add_argument('pathname', help='The directory of the files')
	parser.add_argument('name', help='Name of the zip file')
	# parser.add_argument('-d', '--date', help='date of the files that will be zipped all together in one file', type=valid_date)
	parser.add_argument('-v', '--validate', help='Validate zip file created', action='store_true')

	args = parser.parse_args()

	directory = pathlib.Path(args.pathname)

	if directory.is_dir():

		# Changes the current working directory to the pathname directory
		os.chdir(args.pathname)

		# Filter just the files
		files_to_zip = [content for content in directory.iterdir() if content.is_file()]
		
		current_date = set_date_for_files(files_to_zip)

		while True:
			
			# List to work with files that have the same date
			file_date_zip = []	

			# Using the index to pop from the list of all files in the directory, so it won't be available
			# in the next iteration
			for idx, file in enumerate(files_to_zip):

				# Get the extension, so the program doesn't try to zip a .zip file 
				file_name, extension =  os.path.splitext(file)

				if extension != 'zip' and creation_date(file) == current_date:
					file_date_zip.append(files_to_zip.pop(idx))

			if len(files_to_zip) == 0:
				break;

			if len(file_date_zip) > 0:

				zip_file_name = args.name +  '_{}.zip'.format(current_date)

				with ZipFile(zip_file_name, 'w', ZIP_DEFLATED) as zip_destination_file:

					for files in files_to_zip:
						print('Compactando arquivo: {} dentro do arquivo: {}'.format(files, zip_file_name))
						zip_destination_file.write(files, os.path.basename(files))

					if args.validate:
						is_file_ok = zip_destination_file.testzip()

						if is_file_ok is None: 
							print('Arquivos compactados e validados dentro do arquivo {}'.format(zip_file_name))
							
					else:
						print('Arquivos compactados com sucesso dentro do arquivo {}'.format(zip_file_name))

			current_date = current_date + datetime.timedelta(days=-1)

	else:
		eprint('O caminho "{}" não é um diretório, favor verificar'.format(args.pathname))
