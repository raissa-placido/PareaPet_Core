from abc import ABC, abstractmethod
from typing import Any

class IConexaoDAO(ABC):
    """Interface para operações de conexão e execução no banco."""

    @abstractmethod
    def obter_conexao(self):
        pass

    @abstractmethod
    def executar_comando(self, sql_comando, commit=True, parametros=()) -> Any:
        pass

    @abstractmethod
    def executar_select(self, sql_select, parametros=()) -> list[Any]:
        pass

class ICrudDAO(ABC):
    """Interface usada para o CRUD das entidades."""

    @abstractmethod
    def criar(self, dados: object) -> object:
        pass

    @abstractmethod
    def buscar_id(self, id: int) -> object:
        pass

    @abstractmethod
    def listar(self) -> list[object]:
        pass

    @abstractmethod
    def alterar(self, id: int, novos_dados: object) -> object:
        pass

    @abstractmethod
    def deletar(self, id: int) -> bool:
        pass
