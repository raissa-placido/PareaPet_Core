from enum_pareapet import (EspecieEnum, 
                  FaixaEtariaEnum, 
                  SexoAnimalEnum, 
                  CuidadosEnum, 
                  CondicoesEspecEnum, 
                  PorteEnum, 
                  MoradiaEnum,
                  SociabilidadeEnum,
                  AlocacaoEnum,
                  ComporamentoEnum
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
                 comportamento: ComporamentoEnum,
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

