from run import db
# from model.models import Loja, Funcao, Ambiente, Servico


if __name__ == '__main__':

	from model.models import *

	db.drop_all()
	db.create_all()

	lojas = [
				Loja(nome='Todeschinni - Guarulhos', valor_comissao=1),
				Loja(nome='Favorita - Suzano', valor_comissao=1.25)
			]

	funcoes = [
				Funcao(nome='Administrador'),
				Funcao(nome='Projetista'),
				Funcao(nome='Finalizador'),
				Funcao(nome='Medidor')
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

	db.session.add_all(lojas)
	db.session.add_all(funcoes)
	db.session.add_all(ambientes)
	db.session.add_all(servicos)
	db.session.commit()
	db.session.close()