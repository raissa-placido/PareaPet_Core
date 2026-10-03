from abc import ABC, abstractmethod
from . models import Pet

class ICrudDAO(ABC):

    '''
    Interface usada para o crud das entidades
    '''

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


class PetDAO(ICrudDAO):

    def criar(self, dados):

        novo_pet = Pet(
            dados.nome,
            dados.sexo,
            dados.cond
            )

        return 

    def buscar_id(self, id):
        return super().buscar_id(id)

    def listar(self):
        return super().listar()

    def alterar(self, id, novos_dados):
        return super().alterar(id, novos_dados)

    def deletar(self, id):
        return super().deletar(id)