from abc import ABC, abstractmethod
from typing import List, Optional

try:
    from .models import Adotante, ONG, Pet
except ImportError:
    from models import Adotante, ONG, Pet


class IPetDAO(ABC):
    """Interface de acesso aos dados de Pet."""

    @abstractmethod
    def criar(self, pet: Pet) -> Pet:
        pass

    @abstractmethod
    def buscar_id(self, id: int) -> Optional[Pet]:
        pass

    @abstractmethod
    def listar(self) -> List[Pet]:
        pass

    @abstractmethod
    def alterar(self, id: int, novos_dados: Pet) -> Optional[Pet]:
        pass

    @abstractmethod
    def deletar(self, id: int) -> bool:
        pass


class IONGDAO(ABC):
    """Interface de acesso aos dados de ONG."""

    @abstractmethod
    def criar(self, ong: ONG) -> ONG:
        pass

    @abstractmethod
    def buscar_id(self, id: int) -> Optional[ONG]:
        pass

    @abstractmethod
    def listar(self) -> List[ONG]:
        pass

    @abstractmethod
    def alterar(self, id: int, novos_dados: ONG) -> Optional[ONG]:
        pass

    @abstractmethod
    def deletar(self, id: int) -> bool:
        pass


class IAdotanteDAO(ABC):
    """Interface de acesso aos dados de Adotante."""

    @abstractmethod
    def criar(self, adotante: Adotante) -> Adotante:
        pass

    @abstractmethod
    def buscar_id(self, id: int) -> Optional[Adotante]:
        pass

    @abstractmethod
    def listar(self) -> List[Adotante]:
        pass

    @abstractmethod
    def alterar(self, id: int, novos_dados: Adotante) -> Optional[Adotante]:
        pass

    @abstractmethod
    def deletar(self, id: int) -> bool:
        pass
