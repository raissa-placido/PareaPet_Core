from enum import Enum

class EspecieEnum(Enum):
    GATO = (1, "Gato")
    CACHORRO = (2,"Cachorro")
    OUTRO = (3, "Outro")

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

class SexoAnimalEnum(Enum):
    MACHO = (1, "Macho")
    FEMEA = (2, "Femea")

    def __init__(self, codigo, descricao):
            self.codigo = codigo
            self.descricao = descricao

class PorteEnum(Enum):
    PEQUENO = (1, 'Pequeno')
    MEDIO = (2, 'Medio')
    GRANDE = (3, 'Grande')

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

class MoradiaEnum(Enum):
    CASA = (1, 'Casa')
    APARTAMENTO = (2, 'Apartamento')

    def __init__(self, codigo, descricao):
         self.codigo = codigo
         self.descricao = descricao

class AlocacaoEnum(Enum):
    NA_ONG = (1,'Na ONG')
    NO_LAR_TEMPORARIO = (2, 'No Lar Temporário')
    ADOTADO = (3, 'Adotado')

    def __init__(self, codigo, descricao):
         self.codigo = codigo
         self.descricao = descricao

class TipoUsuarioEnum(Enum):
    ADOTANTE = (1, 'Adotante')
    ONG = (2, 'ONG')
    LAR_TEMPORARIO = (3, 'Lar Temporário')

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

class EstadoBrasileiroEnum(Enum):
    AC = (1, 'Acre')
    AL = (2, 'Alagoas')
    AP = (3, 'Amapá')
    AM = (4, 'Amazonas')
    BA = (5, 'Bahia')
    CE = (6, 'Ceará')
    DF = (7, 'Distrito Federal')
    ES = (8, 'Espírito Santo')
    GO = (9, 'Goiás')
    MA = (10, 'Maranhão')
    MT = (11, 'Mato Grosso')
    MS = (12, 'Mato Grosso do Sul')
    MG = (13, 'Minas Gerais')
    PA = (14, 'Pará')
    PB = (15, 'Paraíba')
    PR = (16, 'Paraná')
    PE = (17, 'Pernambuco')
    PI = (18, 'Piauí')
    RJ = (19, 'Rio de Janeiro')
    RN = (20, 'Rio Grande do Norte')
    RS = (21, 'Rio Grande do Sul')
    RO = (22, 'Rondônia')
    RR = (23, 'Roraima')
    SC = (24, 'Santa Catarina')
    SP = (25, 'São Paulo')
    SE = (26, 'Sergipe')
    TO = (27, 'Tocantins')
    
    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao
    
