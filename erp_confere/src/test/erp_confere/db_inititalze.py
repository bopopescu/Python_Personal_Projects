from run import app, user_datastore
from persistence.mysql_persistence import db



if __name__ == '__main__':

	app.app_context().push()

	# with app.app_context():
	# 	db.init_app(app)

	from model.models import *

	db.drop_all()
	db.create_all()

	lojas = [
				Loja(nome='Todeschinni - Guarulhos', valor_comissao=1),
				Loja(nome='Favorita - Suzano', valor_comissao=1.25)
			]

	# funcoes = [
	# 			Funcao(nome='Administrador'),
	# 			Funcao(nome='Projetista'),
	# 			Funcao(nome='Finalizador'),
	# 			Funcao(nome='Medidor')
	# 		]

	ambientes = [
				Ambiente(nome='Quarto'),
				Ambiente(nome='Sala de Estar'),
				Ambiente(nome='Cozinha'),
				Ambiente(nome='Lavanderia'),
				Ambiente(nome='Sala de Jantar'),
				Ambiente(nome='Banheiro')
			]

	servicos = [
				Servico(codigo=1, nome='medicao', nome_real='Medição', valor='80', sequencia=1, tipo_valor='rl'),
				Servico(codigo=2, nome='subir_paredes', nome_real='Subir Paredes', valor='0.002', 
					sequencia=2, tipo_valor='pct'),
				Servico(codigo=3, nome='projeto', nome_real='Projeto', valor='0.003', 
					sequencia=3, tipo_valor='pct'),
				Servico(codigo=4, nome='atendimento', nome_real='Atendimento', valor='0.003', 
					sequencia=4, tipo_valor='pct'),
				Servico(codigo=5, nome='liberacao', nome_real='Liberação', valor='0.003', 
					sequencia=5, tipo_valor='pct'),
				Servico(codigo=6, nome='manual_de_montagem', nome_real='Manual de Montagem', valor='0.0025', 
					sequencia=6, tipo_valor='pct')
			]
	funcoes = [
		Role(name='admin', description='Administrador do sistema'),
		Role(name='medidor', description='Realiza a medição'),
		Role(name='projetista', description='Realiza os projetos')
	]
	db.session.add_all(lojas)
	# db.session.add_all(funcoes)
	db.session.add_all(ambientes)
	db.session.add_all(servicos)

	# [user_datastore.create_role(name=funcao.name, description=funcao.description) for funcao in funcoes]
	
	marco = user_datastore.create_user(username='marco.han', email='marcohanpsn@gmail.com', password='password')
	vinicius = user_datastore.create_user(username='vinicius.yosiura', email='vinicius.yosiura@live.com', password='password')
	matt = user_datastore.create_user(username='matt', email='matt@nobien.net', password='password')

	user_datastore.add_role_to_user(vinicius, funcoes[0])
	user_datastore.add_role_to_user(marco, funcoes[1])
	user_datastore.add_role_to_user(matt, funcoes[2])

	db.session.commit()
	db.session.close()