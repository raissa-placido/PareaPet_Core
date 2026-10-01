from enum import Enum

class EspecieEnum(Enum):
    GATO = (1, "Gato")
    CACHORRO = (2,"Cachorro")

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao


class FaixaEtariaEnum(Enum):
    ZERO_A_UM = (1, "Até 1 ano")
    DOIS_A_SEIS = (2, "De 2 a 6 anos")
    SETE_MAIS = (3, "7 a mais anos")
    SEM_PREFERENCIA = (4, "Sem preferência de idade")

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

class SexoAnimalEnum(Enum):
    MACHO = (1, "Macho")
    FEMEA = (2, "Femea")

    def __init__(self, codigo, descricao):
            self.codigo = codigo
            self.descricao = descricao

class CuidadosEnum(Enum):
    VACINADO =(1, "Vacinado")
    CASTRADO = (2, "Castrado")
    VERMIFUGADO = (3, "Vermifugado")
    ANTIPULGAS = (4, "Antipulgas")

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

class CondicoesEspecEnum(Enum):
     FIV = (1, "AIDS felina")
     FELV =(2, "Leucemia felina")
     PARALISIA = (3, "Paralisia muscular")
     NEUROLOGICO =(4, " Doença no sistema nervoso")
     CEGUEIRA =(5, "Ausência de visão total ou parcial")
     SURDEZ =(6, "Ausência de audição total ou parcial ")
     OUTRO =(7, " Outras condições especiais")

