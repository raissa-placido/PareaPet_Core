from abc import ABC, abstractmethod
from datetime import date
import json

from dao import ICrudDAO

try:
    from .models import Adotante, ONG, Pet
    from .enum_pareapet import (
        AlocacaoEnum,
        ComportamentoEnum,
        CondicoesEspecEnum,
        CuidadosEnum,
        EspecieEnum,
        FaixaEtariaEnum,
        MoradiaEnum,
        PorteEnum,
        SexoAnimalEnum,
        SociabilidadeEnum,
        TipoUsuarioEnum,
    )
except ImportError:
    from models import Adotante, ONG, Pet
    from enum_pareapet import (
        AlocacaoEnum,
        ComportamentoEnum,
        CondicoesEspecEnum,
        CuidadosEnum,
        EspecieEnum,
        FaixaEtariaEnum,
        MoradiaEnum,
        PorteEnum,
        SexoAnimalEnum,
        SociabilidadeEnum,
        TipoUsuarioEnum,
    )

class IRepository(ICrudDAO):

    @abstractmethod
    def validar(self) -> bool:
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
