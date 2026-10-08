from enum import Enum

class EspecieEnum(Enum):
    GATO = (1, "Gato")
    CACHORRO = (2,"Cachorro")
    OUTRO = (3, "Outro")

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

class ComportamentoEnum(Enum):
    CALMO = (1,'Calmo')
    BRINCALHAO = (2,'Brincalhão')
    INDEPENDENTE = (3, 'Independente')
    CARENTE = (4,'Carente')
    SOCIAVEL = (5,'Sociável')
    APEGADO = (6, 'Apegado')
    DOCIL = (7,'Docil')
    CURIOSO = (8,'Curioso')
    COMPANHEIRO = (9,'Companheiro')
    ANTISSOCIAL = (10,'Antissocial')

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

class SociabilidadeEnum(Enum):
    GATO = (1,'Gato')
    CACHORRO = (2,'Cachorro')
    CRIANCA = (3,'Criança')
    OUTRO_ANIMAL = (4,'Outros animais')

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

class RedesSociaisEnum(Enum):
    WHATSAPP = (1, 'WhatsApp')
    INSTAGRAM = (2, 'Instagram')
    FACEBOOK = (3, 'Facebook')

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

class ExperienciaEnum(Enum):
    INICIANTE = (1, 'Iniciante')
    INTERMEDIARIO = (2, 'Intermediário')
    AVANCADO = (3, 'Avançado')
    NENHUMA = (4, 'Nenhuma')

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

class MotivoDevolucaoEnum(Enum):
    SITUACAO_FINANCEIRA = (1, 'Situação financeira')
    ANIMAL_DESTRUIR_ALGO = (2, 'Animal destruiu algo')
    RECLAMACAO_VIZINHOS = (3, 'Reclamação de vizinhos')
    MUDANCA_DE_CASA = (4, 'Mudança de casa')
    GRAVIDEZ_NA_FAMILIA = (5, 'Gravidez na família')
    NENHUM_MOTIVO = (6, 'Nenhum motivo')

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

class StatusSolicitacaoEnum(Enum):
    PENDENTE = (1, 'Pendente')
    EM_ANALISE = (2, 'Em análise')
    APROVADA = (3, 'Aprovada')
    REJEITADA = (4, 'Rejeitada')
    CANCELADA = (5, 'Cancelada')

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao
