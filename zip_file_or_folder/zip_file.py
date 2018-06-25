# compress the file by name, or part of the name
import os
import argparse
import datetime
import pathlib
import zipfile


def file_exists(filename):
	print('Verificando se o arquivo {} existe: '.format(filename))
	arc = pathlib.Path(filename)
	
	return arc.exists()


def remove_file(filename):

	if file_exists(filename):
		print('Arquivo {} já existe, removendo arquivo'.format(filename))
		os.remove(filename)
	else:
		print('Arquivo {} ainda não existe'.format(filename))

def validate_file(zip_file_obj):

	validation = zip_file_obj.testzip()

	if validation is None:
		print('Arquivo validado com sucesso')
	else:
		print('Arquivo {} esta corrompido'.format(validation))
		sys.exit(1)

def zip_files(files,output_name):

	output_dest_name = output_name+'.zip'
		
	remove_file(output_dest_name)

	print('Compactando os arquivos no arquivo: {}'.format(output_dest_name))
	with zipfile.ZipFile(output_dest_name, 'w', zipfile.ZIP_DEFLATED) as zip_dest_file:
		for file in files:

			print('Compactando o arquivo: {}'.format(file))
			zip_dest_file.write(file, os.path.basename(file))

		print('Validando o arquivo: {}'.format(output_dest_name))	
		validate_file(zip_dest_file)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('path', help="Path on the filesystem which has the files. Must be a directory", type=str)
	parser.add_argument('pattern', help="Pattern which the filename must has to be add to compress", type=str)
	parser.add_argument('outputfile', help='Name of the file which the files will be zipped', type=str)
	parser.add_argument('-v', '--validate', action='store_true', 
		help="If this option is included, the file is only validate. Must be a zip file")

	args = parser.parse_args()

	directory = pathlib.Path(args.path)

	if directory.is_dir():

		print('Alterando para o diretório: {}'.format(directory))
		os.chdir(directory)
		print('Alterado o diretório corrente para: {}'.format(os.getcwd()))

		print('Procurando por arquivos com o mesmo padrão: "{}"'.format(args.pattern))
		files_to_zip = [file for file in directory.iterdir() if file.is_file() and args.pattern in file.name]

		if len(files_to_zip) > 0:
			zip_files(files_to_zip, args.outputfile)
		else:
			print('Nenhum arquivo encontrado com o padrão "{}" para realizar a compactação'.format(args.pattern)) 

		print('Encerrando a execução')

	else:

		print('O caminho especificado não é um diretório',file=sys.stderr)





