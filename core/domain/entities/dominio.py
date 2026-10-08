from enum_pareapet import (EspecieEnum,
                  FaixaEtariaEnum,
                  SexoAnimalEnum,
                  CuidadosEnum,
                  CondicoesEspecEnum,
                  PorteEnum,
                  MoradiaEnum,
                  SociabilidadeEnum,
                  AlocacaoEnum,
                  ComportamentoEnum,
                  TipoUsuarioEnum
                  )

class Pet():

    def __init__(self,
                 id,
                 nome,
                 especie: EspecieEnum,
                 faixa_etaria: FaixaEtariaEnum,
                 cuidados: CuidadosEnum,
                 sexo: SexoAnimalEnum,
                 cond_esp: CondicoesEspecEnum,
                 porte: PorteEnum,
                 moradia: MoradiaEnum,
                 sociabilidade:SociabilidadeEnum,
                 alocacao: AlocacaoEnum,
                 comportamento: ComportamentoEnum,
                 disponivel = True,
                 foto = None,
                 biografia = None,
                 data_nascimento = None,
                ):

        self.id = id
        self.nome = nome
        self.especie = especie
        self.data_nascimento = data_nascimento
        self.faixa_etaria = faixa_etaria
        self.sexo = sexo
        self.cuidados = cuidados
        self.cond_esp = cond_esp
        self.porte = porte
        self.moradia_recomendada = moradia
        self.sociabilidade = sociabilidade
        self.comportamento = comportamento
        self.alocacao = alocacao
        self.fotos = foto
        self.biografia = biografia
        self.disponivel = disponivel




class UsuarioBase():

    def __init__(self,
                 id,
                 tipo_usuario: TipoUsuarioEnum,
                 email,
                 senha,
                 cep,
                 rua,
                 numero,
                 bairro,
                 cidade,
                 estado,
                 telefone,
                 url_foto_perfil = None,
                ):

        self.id = id
        self.url_foto_perfil = url_foto_perfil
        self.tipo_usuario = tipo_usuario
        self.email = email
        self.senha = senha
        self.cep = cep
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.telefone = telefone


class ONG(UsuarioBase):

    def __init__(self,
                 cnpj,
                 razao_social,
                 descricao,
                 pix_para_doacao,
                 **dados_usuario
                ):

        super().__init__(tipo_usuario=TipoUsuarioEnum.ONG, **dados_usuario)
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.descricao = descricao
        self.pix_para_doacao = pix_para_doacao
        self.pets = []


class Adotante(UsuarioBase):

    def __init__(self,
                 cpf,
                 data_nascimento,
                 **dados_usuario
                ):

        super().__init__(tipo_usuario=TipoUsuarioEnum.ADOTANTE, **dados_usuario)
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.pets_solicitados = []
