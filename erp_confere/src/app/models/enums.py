from enum import Enum, unique

@unique
class Status(Enum):
	NOVO='novo'
	INICIADO='iniciado'
	AGENDADO='agendado'
	CONCLUIDO='concluido'
