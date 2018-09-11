from urllib.parse import quote_plus
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.dialects.mysql as mysqldialect
import datetime


engine = create_engine('mysql+mysqldb://python:%s@192.168.33.50/alchemy' % quote_plus('Senh@1ndefinid4'), echo=True)

Base = declarative_base()


class Funcao(Base):
	__tablename__ = 'funcao'

	codigo = Column('cd_funcao', Integer, primary_key=True, nullable=False)
	nome = Column('nm_funcao', String(45), nullable=False)

class Funcionario(Base):
	__tablename__ = 'funcionario'
	__table_args__ = ((PrimaryKeyConstraint('cd_funcionario', name='pk_funcionario'),))

	codigo = Column('cd_funcionario', Integer, nullable=False)
	nome = Column('nm_funcionario', String(45), nullable=False)
	sobrenome = Column('sobre_nm_funcionario', String(45), nullable=False)
	data_admissao = Column('dt_admissao', mysqldialect.DATE, nullable=False)
	data_demissao = Column('dt_demissao', mysqldialect.DATE)
	telefone_residencial = Column('nr_telefone_res', mysqldialect.BIGINT)
	telefone_celular = Column('nr_telefone_cel', mysqldialect.BIGINT)
	cargo = Column('ds_cargo', mysqldialect.ENUM('socio', 'finalizador', 'projetista', 'medidor', 'secretaria'), nullable=False)

class Usuario(Base):
	__tablename__ = 'usuario'
	__table_args__ = (PrimaryKeyConstraint('cd_usuario', name='PK_USUARIO'),)

	codigo = Column('cd_usuario', Integer, ForeignKey('funcionario.cd_funcionario', name='fk_usuario_has_funcionario'),nullable=False)
	username = Column('ds_username', String(45), nullable=False)
	password = Column('ds_password', String(45), nullable=False)
	data_criacao = Column('dt_criacao', mysqldialect.DATETIME, nullable=False, default=datetime.datetime.utcnow())
	data_alteracao = Column('dt_alteracao', mysqldialect.DATETIME, nullable=False, default=datetime.datetime.utcnow())
	funcao = Column('cd_funcao', Integer, ForeignKey('funcao.cd_funcao', name='fk_funcionario_has_funcao'), nullable=False)
	funcao_obj = relationship('Funcao')
	funcionario_obj = relationship('Funcionario')

class Loja(Base):
	__tablename__ = 'loja'

	codigo = Column('cd_loja', Integer, primary_key=True, nullable=False)
	nome = Column('nm_loja', String(45), nullable=False)
	valor_comissao = Column('valor_comissao', mysqldialect.DECIMAL(precision=10, scale=2), nullable=False, default=0)

class Cep(Base):
	__tablename__ = 'cep'

	numero = Column('nr_cep', String(8), primary_key=True, autoincrement=False, nullable=False)
	logradouro = Column('logradouro', String(100), nullable=False)
	complemento = Column('complemento', String(45))
	bairro = Column('bairro', String(45), nullable=False)
	cidade = Column('cidade', String(45), nullable=False)
	uf = Column('uf', String(2), nullable=False)

class ClienteEndereco(Base):
	__tablename__ = 'cliente_endereco'

	codigo = Column('cd_cliente_endereco', Integer, primary_key=True, nullable=False)
	cep = Column('cep', String(8), ForeignKey('cep.nr_cep', name='fk_cliente_endereco_has_cep'), nullable=False)
	cep_obj = relationship('Cep')
	cliente = Column('cd_cliente', Integer, 
		ForeignKey('cliente.cd_cliente', name='fk_cliente_endereco_has_cliente'), nullable=False)
	cliente_obj = relationship('Cliente')
	numero = Column('nr_endereco', Integer, nullable=False)
	complemento = Column('ds_complemento', String(120))
	referencia = Column('ds_referencia', String(255))

class Cliente(Base):
	__tablename__ = 'cliente'

	codigo = Column('cd_cliente', Integer, primary_key=True, nullable=False)
	nome = Column('nm_cliente', String(45), nullable=False)
	sobrenome = Column('sobre_nm_cliente', String(45), nullable=False)
	email = Column('ds_email', String(80), nullable=False)
	telefone_residencial = Column('nr_telefone_res', mysqldialect.BIGINT)
	telefone_celular = Column('nr_telefone_cel', mysqldialect.BIGINT, nullable=False)

class Ambiente(Base):
	__tablename__ = 'ambiente'
	__table_args__ = (UniqueConstraint('nm_ambiente', name='UQ_NM_AMBIENTE'), )

	codigo = Column('cd_ambiente', Integer, primary_key=True, nullable=False)
	nome = Column('nm_ambiente', String(30), nullable=False)

class Servico(Base):
	__tablename__ = 'servico'
	__table_args__ = (PrimaryKeyConstraint('cd_servico', name='pk_servico'),)

	codigo = Column('cd_servico', Integer, nullable=False, autoincrement=False)
	nome = Column('nm_servico', String(30), nullable=False)
	nome_real = Column('nm_servico_real', String(30), nullable=False)
	valor = Column('vl_servico', mysqldialect.DECIMAL(precision=10,scale=2), nullable=False, default=0)
	sequencia = Column('nr_sequencia', Integer, nullable=False)
	tipo_valor_servico = Column('tp_vl_servico', mysqldialect.ENUM('pct', 'rl'), default='pct', nullable=False)

class Pedido(Base):
	__tablename__ = 'pedido'
	__table_args__ = (PrimaryKeyConstraint('cd_pedido', name='pk_pedido'),)

	codigo = Column('cd_pedido', Integer, nullable=False)
	cliente_endereco = Column('cd_cliente_endereco', Integer, 
		ForeignKey('cliente_endereco.cd_cliente_endereco', name='fk_pedido_has_cliente_endereco'), nullable=False)
	cliente_endereco_obj = relationship('ClienteEndereco')
	loja = Column('cd_loja', Integer, ForeignKey('loja.cd_loja', name='fk_pedido_has_loja'), nullable=False)
	loja_obj = relationship('Loja')
	complemento = Column('cd_pedido_pai', Integer, ForeignKey('pedido.cd_pedido', name='fk_pedido_has_pedido'))
	complemento_obj = relationship('Pedido')
	numero = Column('nr_pedido', String(20), nullable=False)
	valor = Column('vl_pedido', mysqldialect.DECIMAL(precision=10,scale=2), nullable=False)
	data_entrada = Column('dt_entrada', mysqldialect.DATE, nullable=False)
	data_inicio = Column('dt_inicio', mysqldialect.DATE)
	data_fim = Column('dt_fim', mysqldialect.DATE)
	ambientes = Column('ambientes', mysqldialect.JSON, nullable=False)

class PedidoServico(Base):
	__tablename__ = 'pedido_servico'
	__table_args__ = ((PrimaryKeyConstraint('cd_pedido', 'cd_servico', name='pk_pedido_servico'),))

	pedido = Column('cd_pedido', Integer, ForeignKey('pedido.cd_pedido', name='fk_pedido_servico_has_pedido'), 
		nullable=False)
	pedido_obj = relationship('Pedido')
	servico = Column('cd_servico', Integer, ForeignKey('servico.cd_servico', name='fk_pedido_servico_has_servico'),
		nullable=False)
	servico_obj = relationship('Servico')
	funcionario = Column('cd_funcionario', Integer, 
		ForeignKey('funcionario.cd_funcionario', name='fk_pedido_servico_has_funcionario'))
	funcionario_obj = relationship('Funcionario')
	valor_comissao = Column('vl_comissao', mysqldialect.DECIMAL(precision=10,scale=2), nullable=False, default=0)
	data_inicio = Column('dt_inicio', mysqldialect.DATE)
	data_fim = Column('dt_fim', mysqldialect.DATE)
	servico_props = Column('servico_props', mysqldialect.JSON)


if __name__ == '__main__':

	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)


