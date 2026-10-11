from abc import ABC, abstractmethod

class IRepository(ABC):

    @abstractmethod
    def validar(self, obj: object) -> bool:
        pass

    @abstractmethod
    def criar(self, obj: object) -> object:
        pass

    @abstractmethod
    def buscar_id(self, id: int) -> object:
        pass

    @abstractmethod
    def listar(self) -> list[object]:
        pass

    @abstractmethod
    def alterar(self, id: int, obj: object) -> object:
        pass

    @abstractmethod
    def deletar(self, id: int) -> bool:
        pass
