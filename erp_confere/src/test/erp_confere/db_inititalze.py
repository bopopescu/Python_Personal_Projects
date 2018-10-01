#!/usr/bin/env python3

from run import app, user_datastore
from persistence.mysql_persistence import db
from datetime import date
from app_util.feriados import feriados

if __name__ == '__main__':

	app.app_context().push()

	from model.models import *

	db.drop_all()
	db.create_all()

	lojas = [
				Loja(nome='Todeschinni - Guarulhos', valor_comissao=1),
				Loja(nome='Favorita - Suzano', valor_comissao=1.25)
			]

	ambientes = [
				Ambiente(nome='Quarto'),
				Ambiente(nome='Sala de Estar'),
				Ambiente(nome='Cozinha'),
				Ambiente(nome='Lavanderia'),
				Ambiente(nome='Sala de Jantar'),
				Ambiente(nome='Banheiro')
			]

	servicos = [
				Servico(codigo=1, nome='medicao', nome_real='Medição', valor='80', sequencia=1, tipo_valor='rl', dias_servico=3),
				Servico(codigo=2, nome='subir_paredes', nome_real='Subir Paredes', valor='0.002', 
					sequencia=2, tipo_valor='pct', dias_servico=5),
				Servico(codigo=3, nome='projeto', nome_real='Projeto', valor='0.003', 
					sequencia=3, tipo_valor='pct', dias_servico=4),
				Servico(codigo=4, nome='atendimento', nome_real='Atendimento', valor='0.003', 
					sequencia=4, tipo_valor='pct', dias_servico=6),
				Servico(codigo=5, nome='liberacao', nome_real='Liberação', valor='0.003', 
					sequencia=5, tipo_valor='pct', dias_servico=7),
				Servico(codigo=6, nome='manual_de_montagem', nome_real='Manual de Montagem', valor='0.0025', 
					sequencia=6, tipo_valor='pct', dias_servico=10)
			]
	
	funcoes = [
		Role(name='admin', description='Administrador do sistema'),
		Role(name='medidor', description='Realiza a medição'),
		Role(name='projetista', description='Realiza os projetos'),
		Role(name='controladora', description='Controla os pedidos servicos')
	]



	new_user = User(email='vinicius.yosiura@gmail.com', username='vinicius.yosiura', roles=[funcoes[0]],
		password='password')
	new_funcionario = Funcionario(nome='Vinicius', sobrenome='Akiyama Hashizumi Yosiura', 
		telefone_celular='11979863277',	cargo='socio', usuario=new_user, data_admissao=date.today())
	db.session.add_all(lojas)
	db.session.add_all(ambientes)
	db.session.add_all(servicos)
	db.session.add_all(funcoes)
	db.session.add_all(feriados)
	db.session.add(new_user)
	db.session.add(new_funcionario)


	db.session.commit()

	db.session.close()