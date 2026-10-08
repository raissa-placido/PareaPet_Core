from abc import ABC, abstractmethod
from datetime import date
import re

from dao import ICrudDAO

try:
    from .models import Adotante, ONG, Pet
except ImportError:
    from models import Adotante, ONG, Pet

class IRepository(ABC):

    @abstractmethod
    def validar(self) -> bool:
        pass

    @abstractmethod
    def criar(self, dados) -> object:
        pass

    @abstractmethod
    def buscar_id(self, id) -> object:
        pass

    @abstractmethod
    def listar(self) -> list:
        pass

    @abstractmethod
    def alterar(self, id, novos_dados) -> object:
        pass

    @abstractmethod
    def deletar(self, id) -> bool:
        pass

class PetRepository(IRepository):
    def __init__(self, pet_dao: ICrudDAO):
        self.pet_dao = pet_dao

    def validar(self, pet: Pet) -> bool:
        erros = {}

        if not pet.nome or not pet.nome.strip():
            erros['nome'] = 'O nome do animal não pode ficar em branco.'

        if pet.data_nascimento:
            if pet.data_nascimento > date.today():
                erros['data_nascimento'] = 'A data de nascimento não pode estar no futuro.'

        if erros:
            raise Exception(erros)
            
        # Limpeza de espaços em branco sobrando
        if pet.nome:
            pet.nome = pet.nome.strip()
        if pet.biografia:
            pet.biografia = pet.biografia.strip()

    def criar(self, pet: Pet) -> Pet:
        self.validar(pet)
        return self.pet_dao.criar(pet)

    def buscar_id(self, pet_id: int) -> Pet:
        resultado = self.pet_dao.buscar_id(pet_id)
        
        if resultado is None:
            raise Exception(f"Pet com 'id={pet_id}' não encontrado.")
        
        return resultado
    
    def alterar(self, pet: Pet) -> Pet:
        self.validar(pet)
        return self.pet_dao.alterar(pet)
    
    def deletar(self, pet: Pet) -> bool:
        return self.pet_dao.deletar(pet)

    def listar(self, pet: Pet) -> list:
        return self.pet_dao.listar(pet)

class OngRepository(IRepository):
    def __init__(self, ong_dao: ICrudDAO):
        self.ong_dao = ong_dao

    def validar(self, ong: ONG) -> bool:
        # Padronização (só executa se os dados estiverem válidos)
        if self.cnpj:
            self.cnpj = re.sub(r'[^\d]', '', self.cnpj)

    def criar(self, ong: ONG) -> ONG:
        self.validar(ong)
        return self.ong_dao.criar(ong)
        
    def buscar_id(self, ong_id: int) -> ONG:
        resultado = self.ong_dao.buscar_id(ong_id)
        
        if resultado is None:
            raise Exception(f"ONG com 'id={ong_id}' não encontrada.")
        
        return resultado

    def alterar(self, ong: ONG) -> ONG:
        self.validar(ong)
        return self.ong_dao.alterar(ong)

    def deletar(self, ong: ONG) -> bool:
        return self.ong_dao.deletar(ong)

    def listar(self, ong: ONG) -> list:
        return self.ong_dao.listar(ong)

class AdotanteRepository(IRepository):
    def __init__(self, adotante_dao: ICrudDAO):
        self.adotante_dao = adotante_dao

    def validar(self, adotante: Adotante) -> bool:
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
            raise Exception(f"Erros de validação: {erros}")

        # 2. Limpeza do CPF (Salva apenas números)
        if self.cpf:
            self.cpf = re.sub(r'[^\d]', '', self.cpf)

    def criar(self, adotante: Adotante) -> Adotante:
        self.validar(adotante)
        return self.adotante_dao.criar(adotante)

    def buscar_id(self, adotante_id: int) -> Adotante:
        resultado = self.adotante_dao.buscar_id(adotante_id)
        
        if resultado is None:
            raise Exception(f"Adotante com 'id={adotante_id}' não encontrado.")
        
        return resultado

    def alterar(self, adotante: Adotante) -> Adotante:
        self.validar(adotante)
        return self.adotante_dao.alterar(adotante)

    def deletar(self, adotante: Adotante) -> bool:
        return self.adotante_dao.deletar(adotante)  

    def listar(self, adotante: Adotante) -> list:
        return self.adotante_dao.listar(adotante)