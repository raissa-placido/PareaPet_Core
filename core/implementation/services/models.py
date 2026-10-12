from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

import re
from datetime import date

from core.domain.entities.enums import (
    AlocacaoEnum,
    EspecieEnum,
    EstadoBrasileiroEnum,
    MoradiaEnum,
    PorteEnum,
    SexoAnimalEnum,
    TipoUsuarioEnum,
)
from .utils.validators import validar_cep, validar_cidade, validar_cpf, validar_cnpj, validar_nome


def _enum_choices(enum_class):
    return [(item.codigo, item.descricao) for item in enum_class]


## Modelo Usúario base

class UsuarioBase(AbstractUser):
    # Validação de formato de imagem permitida (evita arquivos maliciosos ou não suportados)
    foto_perfil = models.ImageField(
        upload_to='imgs/perfil/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    tipo_usuario = models.IntegerField(
        choices=_enum_choices(TipoUsuarioEnum), null=True, blank=True
    )
    
    # Aplicação do validador de CEP
    cep = models.CharField(
        max_length=9, 
        blank=True, 
        null=True, 
        validators=[validar_cep]
    )
    rua = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        validators=[validar_cidade]
    )
    estado = models.IntegerField(
        choices=_enum_choices(EstadoBrasileiroEnum), null=True, blank=True
    )
    telefone = models.CharField(max_length=20,blank=True,null=True)


    def clean(self):
        super().clean()
        erros = {}
        
        #Validação de telefone
        if self.telefone:
            telefone_limpo = re.sub(r'[^\d+]', '', self.telefone)

            if len(telefone_limpo) < 10 or len(telefone_limpo) > 15:
                erros['telefone'] = (
                    'Informe um telefone válido com DDD '
                    '(mínimo 10 dígitos).'
                )
            else:
                self.telefone = telefone_limpo
                
        # 1. Validação de Endereço Parcial: 
        # Se o usuário preencher qualquer campo do endereço, ele deve preencher os fundamentais.
        campos_endereco = [self.rua, self.numero, self.bairro]
        tem_algum_campo = any(campos_endereco)
        todos_campos = all(campos_endereco)

        if tem_algum_campo and not todos_campos:
            mensagem_erro = "Se for cadastrar um endereço, os campos Rua, Número e Bairro são obrigatórios."
            if not self.rua:
                erros['rua'] = mensagem_erro
            if not self.numero:
                erros['numero'] = mensagem_erro
            if not self.bairro:
                erros['bairro'] = mensagem_erro

        # Lança os erros agrupados (aparecerão corretamente nos forms/admin)
        if erros:
            raise ValidationError(erros)

    def __str__(self):
        full_name = self.get_full_name().strip()
        return full_name if full_name else self.username

    @property
    def endereco_formatado(self):
        partes_endereco = []
        if self.rua:
            partes_endereco.append(self.rua)
        if self.numero:
            partes_endereco.append(self.numero)
        if self.bairro:
            partes_endereco.append(self.bairro)
        
        # Junta rua, numero e bairro com vírgulas (ex: "Rua A, 123, Centro")
        endereco_base = ", ".join(partes_endereco) if partes_endereco else "Endereço não informado"

        # Formata o CEP se ele existir
        cep_formatado = f" CEP: {self.cep}" if self.cep else ""

        # Formata a Cidade e o Estado
        # Nota: Como 'estado' usa choices (provavelmente uma Enum), usamos 'get_estado_display()' para pegar o nome/sigla
        localidade = ""
        if self.cidade or self.estado is not None:
            cidade_str = self.cidade if self.cidade else ""
            estado_str = self.get_estado_display() if self.estado is not None else ""
            
            if cidade_str and estado_str:
                localidade = f". {cidade_str}-{estado_str}"
            elif cidade_str or estado_str:
                localidade = f". {cidade_str}{estado_str}"

        return f"{endereco_base}{cep_formatado}{localidade}".strip()
    
    
## Modelo Adotante
    
class Adotante(models.Model):
    adotante = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adotante')
    nome = models.CharField(max_length=50, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True, validators=[validar_cpf])
    data_nascimento = models.DateField(null=True, blank=True)

    def clean(self):
        super().clean()
        erros = {}

        # 1. Validação de Idade (Ex: Usuário precisa ser maior de 18 anos)
        if self.data_nascimento:
            hoje = date.today()
            idade = hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
            
            if idade < 18:
                erros['data_nascimento'] = 'O usuário precisa ter pelo menos 18 anos.'
            elif self.data_nascimento > hoje:
                erros['data_nascimento'] = 'A data de nascimento não pode estar no futuro.'

        if erros:
            raise ValidationError(erros)

        # 2. Limpeza do CPF (Salva apenas números)
        if self.cpf:
            self.cpf = re.sub(r'[^\d]', '', self.cpf)

    def __str__(self):
        return self.nome or self.adotante.username
    
    
## Modelo ONG

class ONG(models.Model):
    ong = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ong')
    cnpj = models.CharField(max_length=18, unique=True, validators=[validar_cnpj])
    pix_doacao = models.CharField(max_length=50, blank=True)
    razao_social = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)

    def clean(self):
        super().clean()
        
        # 1. Cria o dicionário para acumular os erros
        erros = {}
        
        # Validação do PIX
        #if self.pix_doacao and len(self.pix_doacao.strip()) < 5:
        #    erros['pix_doacao'] = 'A chave PIX informada é muito curta.'
            
        # Validação da Descrição
        #if not self.descricao or not self.descricao.strip():
        #    erros['descricao'] = 'A descrição não pode ficar em branco.'

        # 2. Se houver qualquer erro acumulado, levanta a exceção com todos eles de uma vez
        if erros:
            raise ValidationError(erros)
            
        # Padronização (só executa se os dados estiverem válidos)
        if self.cnpj:
            self.cnpj = re.sub(r'[^\d]', '', self.cnpj)

    def __str__(self):
        return f'{self.razao_social} ({self.cnpj})'
    

# Modelo de Pet



class Pet(models.Model):
    ong = models.ForeignKey(ONG, on_delete=models.PROTECT, related_name='pets_mantidos')
    especie = models.IntegerField(choices=_enum_choices(EspecieEnum))
    nome = models.CharField(max_length=100, validators=[validar_nome])
    sexo = models.IntegerField(choices=_enum_choices(SexoAnimalEnum))
    data_nascimento = models.DateField(null=True, blank=True)
    alocacao = models.IntegerField(choices=_enum_choices(AlocacaoEnum))
    porte = models.IntegerField(choices=_enum_choices(PorteEnum))
    moradia_recomendada= models.IntegerField(choices=_enum_choices(MoradiaEnum))
    disponivel = models.BooleanField(default=True)
    biografia = models.TextField(blank=True, null=True)

    def clean(self):
        super().clean()
        erros = {}

        if not self.nome or not self.nome.strip():
            erros['nome'] = 'O nome do animal não pode ficar em branco.'

        if self.data_nascimento:
            if self.data_nascimento > date.today():
                erros['data_nascimento'] = 'A data de nascimento não pode estar no futuro.'

        if erros:
            raise ValidationError(erros)
            
        # Limpeza de espaços em branco sobrando
        if self.nome:
            self.nome = self.nome.strip()
        if self.biografia:
            self.biografia = self.biografia.strip()

    @property
    def calcular_idade_pet(self):
        if not self.data_nascimento:
            return None
        idade_anos = (date.today() - self.data_nascimento).days // 365
        return idade_anos


    def __str__(self):
        return f'{self.nome} ({self.get_especie_display()})'