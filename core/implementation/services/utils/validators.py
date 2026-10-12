import re
from django.core.exceptions import ValidationError

def validar_cnpj(value):
    """Valida se a string passada é um CNPJ válido."""
    cnpj = re.sub(r'[^\d]', '', str(value))
    
    if not cnpj:
        return

    if len(cnpj) != 14:
        raise ValidationError('O CNPJ deve conter exatamente 14 números.')
        
    if cnpj in [str(i) * 14 for i in range(10)]:
        raise ValidationError('O formato do CNPJ é inválido.')
        
    # Cálculo do 1º dígito
    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_1 = sum(int(d) * p for d, p in zip(cnpj[:12], pesos_1))
    r_1 = soma_1 % 11
    d1 = 0 if r_1 < 2 else 11 - r_1
    
    # Cálculo do 2º dígito
    pesos_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_2 = sum(int(d) * p for d, p in zip(cnpj[:13], pesos_2))
    r_2 = soma_2 % 11
    d2 = 0 if r_2 < 2 else 11 - r_2
    
    if cnpj[-2:] != f"{d1}{d2}":
        raise ValidationError('O CNPJ informado é inválido.')


def validar_cpf(value):
    cpf = re.sub(r'[^\d]', '', str(value))
    
    if not cpf:
        return

    if len(cpf) != 11:
        raise ValidationError('O CPF deve conter exatamente 11 números.')
        
    if cpf in [str(i) * 11 for i in range(10)]:
        raise ValidationError('O formato do CPF é inválido.')
        
    # Validação do 1º dígito
    soma_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = 11 - (soma_1 % 11)
    d1 = 0 if d1 > 9 else d1
    
    # Validação do 2º dígito
    soma_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = 11 - (soma_2 % 11)
    d2 = 0 if d2 > 9 else d2
    
    if cpf[-2:] != f"{d1}{d2}":
        raise ValidationError('O CPF informado é inválido.')


def validar_cep(value):
    """Valida se a string passada é um CEP válido."""
    if not value:
        return
        
    if not re.match(r'^\d{5}-?\d{3}$', str(value)):
        raise ValidationError("O CEP deve estar no formato XXXXX-XXX ou XXXXXXXX (apenas números).")

def validar_cidade(value):
    """Valida se a cidade contém apenas letras e caracteres permitidos."""
    if not value:
        return

    if not re.match(r"^[a-zA-ZÀ-ÿ\s\-\']+$", str(value)):
        raise ValidationError("O campo cidade deve conter apenas letras.")


def validar_nome(value):
    """Valida se o nome contém apenas letras e caracteres permitidos."""
    if not value:
        return

    if not re.match(r"^[a-zA-ZÀ-ÿ\s\-\']+$", str(value)):
        raise ValidationError("O campo nome deve conter apenas letras.")