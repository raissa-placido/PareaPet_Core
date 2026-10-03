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

class ComporamentoEnum(Enum):
    CALMO = (1,'Calmo')
    BRINCALHAO = (2,'Brincalhão')
    INDEPENDENTE = (3, 'Independente')
    CARENTE = (4,'Carente')
    SOCIAVEL = (5,'Sociael')
    APEGADO = (6, 'Apegado')
    DOCIL = (7,'Docil')
    CURIOSO = (8,'Curioso')
    COMPANHEIRO = (9,'Companheiro')
    ANTISSOCIAL = (10,'Antissocial')

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

class AlocacaoEnum(Enum):
    ONG = (1,'Na ONG')
    LAR_TEMPORARIO = (2, 'No Lar Temporário')
    
    def __init__(self, codigo, descricao):
         self.codigo = codigo
         self.descricao = descricao

class SociabilidadeEnum(Enum):
    GATO = (1,'Gato')
    CACHORRO = (2,'Cachorro')
    CRIANCA = (3,'Crinça')
    OUTRO_ANIMAL = (2,'Outros animais')

    def __init__(self, codigo, descricao):
         self.codigo = codigo
         self.descricao = descricao