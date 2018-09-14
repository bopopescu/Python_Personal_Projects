from urllib.parse import quote_plus
from flask_security import UserMixin, RoleMixin
import sqlalchemy.dialects.mysql as mysqldialect
import sqlalchemy.ext.mutable as mutable
import datetime
from persistence.mysql_persistence import db

class Role(db.Model, RoleMixin):
    __tablename__ = 'funcao'
    __table_args__ = (db.PrimaryKeyConstraint('cd_funcao', name='pk_funcao'), db.UniqueConstraint('nm_funcao', name='uq_nm_funcao'))

    id = db.Column('cd_funcao', db.Integer, nullable=False)
    name = db.Column('nm_funcao', db.String(80), nullable=False)
    description = db.Column('ds_funcao', db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'usuario'
    __table_args__ = (db.PrimaryKeyConstraint('cd_usuario', name='pk_funcao'), db.UniqueConstraint('ds_email', name='uq_ds_email'))


    id = db.Column('cd_usuario', db.Integer, nullable=False)
    email = db.Column('ds_email', db.String(255), nullable=False)
    username = db.Column('nm_usuario', db.String(255))
    password = db.Column('ds_senha', db.String(255), nullable=False)
    last_login_at = db.Column('ds_ultimo_login', mysqldialect.DATETIME)
    current_login_at = db.Column('ds_recente_login', mysqldialect.DATETIME)
    last_login_ip = db.Column('ds_ultimo_ip_login', db.String(100))
    current_login_ip = db.Column('ds_recente_ip_login', db.String(100))
    login_count = db.Column('nr_qtde_login', db.Integer)
    active = db.Column('ativo', mysqldialect.TINYINT(1))
    confirmed_at = db.Column('dt_hr_email_confirmado', mysqldialect.DATETIME)
    roles = db.relationship('Role', secondary='funcao_usuario',
                         backref=db.backref('users', lazy='dynamic'))

class RolesUsers(db.Model):
    __tablename__ = 'funcao_usuario'
    __table_args__ = (db.PrimaryKeyConstraint('cd_funcao_usuario', name='pk_funcao_usuario'),)
    
    id = db.Column('cd_funcao_usuario', db.Integer)
    user_id = db.Column('cd_usuario', db.Integer, db.ForeignKey('usuario.cd_usuario', name='fk_funcao_usuario_has_usuario'), nullable=False)
    role_id = db.Column('cd_funcao', db.Integer, db.ForeignKey('funcao.cd_funcao', name='fk_funcao_usuario_has_funcao'), nullable=False)


class Funcionario(db.Model):
	__tablename__ = 'funcionario'
	__table_args__ = ((db.PrimaryKeyConstraint('cd_funcionario', name='pk_funcionario'),))

	codigo = db.Column('cd_funcionario', db.Integer, nullable=False)
	nome = db.Column('nm_funcionario', db.String(45), nullable=False)
	sobrenome = db.Column('sobre_nm_funcionario', db.String(45), nullable=False)
	data_admissao = db.Column('dt_admissao', mysqldialect.DATE, nullable=False)
	data_demissao = db.Column('dt_demissao', mysqldialect.DATE)
	telefone_residencial = db.Column('nr_telefone_res', mysqldialect.BIGINT)
	telefone_celular = db.Column('nr_telefone_cel', mysqldialect.BIGINT)
	cargo = db.Column('ds_cargo', mysqldialect.ENUM('socio', 'finalizador', 'projetista', 'medidor', 'secretaria'), nullable=False)

class Loja(db.Model):
	__tablename__ = 'loja'

	codigo = db.Column('cd_loja', db.Integer, primary_key=True, nullable=False)
	nome = db.Column('nm_loja', db.String(45), nullable=False)
	valor_comissao = db.Column('valor_comissao', mysqldialect.DECIMAL(precision=10, scale=2), nullable=False, default=0)

class Cep(db.Model):
	__tablename__ = 'cep'

	numero = db.Column('nr_cep', db.String(8), primary_key=True, autoincrement=False, nullable=False)
	logradouro = db.Column('logradouro', db.String(100), nullable=False)
	complemento = db.Column('complemento', db.String(45))
	bairro = db.Column('bairro', db.String(45), nullable=False)
	cidade = db.Column('cidade', db.String(45), nullable=False)
	uf = db.Column('uf', db.String(2), nullable=False)

class ClienteEndereco(db.Model):
	__tablename__ = 'cliente_endereco'

	codigo = db.Column('cd_cliente_endereco', db.Integer, primary_key=True, nullable=False)
	cep = db.Column('cep', db.String(8), db.ForeignKey('cep.nr_cep', name='fk_cliente_endereco_has_cep'), nullable=False)
	cep_obj = db.relationship('Cep')
	cliente = db.Column('cd_cliente', db.Integer, 
		db.ForeignKey('cliente.cd_cliente', name='fk_cliente_endereco_has_cliente'), nullable=False)
	cliente_obj = db.relationship('Cliente')
	numero = db.Column('nr_endereco', db.Integer, nullable=False)
	complemento = db.Column('ds_complemento', db.String(120))
	referencia = db.Column('ds_referencia', db.String(255))

class Cliente(db.Model):
	__tablename__ = 'cliente'

	codigo = db.Column('cd_cliente', db.Integer, primary_key=True, nullable=False)
	nome = db.Column('nm_cliente', db.String(45), nullable=False)
	sobrenome = db.Column('sobre_nm_cliente', db.String(45), nullable=False)
	email = db.Column('ds_email', db.String(80), nullable=False)
	telefone_residencial = db.Column('nr_telefone_res', mysqldialect.BIGINT)
	telefone_celular = db.Column('nr_telefone_cel', mysqldialect.BIGINT, nullable=False)

class Ambiente(db.Model):
	__tablename__ = 'ambiente'
	__table_args__ = (db.UniqueConstraint('nm_ambiente', name='UQ_NM_AMBIENTE'), )

	codigo = db.Column('cd_ambiente', db.Integer, primary_key=True, nullable=False)
	nome = db.Column('nm_ambiente', db.String(30), nullable=False)

class Servico(db.Model):
	__tablename__ = 'servico'
	__table_args__ = (db.PrimaryKeyConstraint('cd_servico', name='pk_servico'),)

	codigo = db.Column('cd_servico', db.Integer, nullable=False, autoincrement=False)
	nome = db.Column('nm_servico', db.String(30), nullable=False)
	nome_real = db.Column('nm_servico_real', db.String(30), nullable=False)
	valor = db.Column('vl_servico', mysqldialect.DECIMAL(precision=12,scale=6), nullable=False, default=0)
	sequencia = db.Column('nr_sequencia', db.Integer, nullable=False)
	tipo_valor = db.Column('tp_vl_servico', mysqldialect.ENUM('pct', 'rl'), default='pct', nullable=False)

class Pedido(db.Model):
	__tablename__ = 'pedido'
	__table_args__ = (db.PrimaryKeyConstraint('cd_pedido', name='pk_pedido'),)

	codigo = db.Column('cd_pedido', db.Integer, nullable=False)
	cliente_endereco = db.Column('cd_cliente_endereco', db.Integer, 
		db.ForeignKey('cliente_endereco.cd_cliente_endereco', name='fk_pedido_has_cliente_endereco'), nullable=False)
	cliente_endereco_obj = db.relationship('ClienteEndereco')
	loja = db.Column('cd_loja', db.Integer, db.ForeignKey('loja.cd_loja', name='fk_pedido_has_loja'), nullable=False)
	loja_obj = db.relationship('Loja')
	complemento = db.Column('cd_pedido_pai', db.Integer, db.ForeignKey('pedido.cd_pedido', name='fk_pedido_has_pedido'))
	complemento_obj = db.relationship('Pedido')
	numero = db.Column('nr_pedido', db.String(20), nullable=False)
	valor = db.Column('vl_pedido', mysqldialect.DECIMAL(precision=10,scale=2), nullable=False)
	data_entrada = db.Column('dt_entrada', mysqldialect.DATE, nullable=False)
	data_inicio = db.Column('dt_inicio', mysqldialect.DATE)
	data_fim = db.Column('dt_fim', mysqldialect.DATE)
	ambientes = db.Column('ambientes', mutable.MutableDict.as_mutable(mysqldialect.JSON), nullable=False)

class PedidoServico(db.Model):
	__tablename__ = 'pedido_servico'
	__table_args__ = ((db.PrimaryKeyConstraint('cd_pedido', 'cd_servico', name='pk_pedido_servico'),))

	pedido = db.Column('cd_pedido', db.Integer, db.ForeignKey('pedido.cd_pedido', name='fk_pedido_servico_has_pedido'), 
		nullable=False)
	pedido_obj = db.relationship('Pedido')
	servico = db.Column('cd_servico', db.Integer, db.ForeignKey('servico.cd_servico', name='fk_pedido_servico_has_servico'),
		nullable=False)
	servico_obj = db.relationship('Servico')
	funcionario = db.Column('cd_funcionario', db.Integer, 
		db.ForeignKey('funcionario.cd_funcionario', name='fk_pedido_servico_has_funcionario'))
	funcionario_obj = db.relationship('Funcionario')
	valor_comissao = db.Column('vl_comissao', mysqldialect.DECIMAL(precision=10,scale=2), nullable=False, default=0)
	data_inicio = db.Column('dt_inicio', mysqldialect.DATE)
	data_fim = db.Column('dt_fim', mysqldialect.DATE)
	servico_props = db.Column('servico_props', mutable.MutableDict.as_mutable(mysqldialect.JSON))