from enum import Enum


class Status(Enum):
    ATIVO = 1
    INATIVO = 2
    DELETADO = 3


class UserStatus(Enum):
    ATIVO = 1
    INATIVO = 2
    DEMITIDO = 3
    FERIAS = 4
