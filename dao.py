from abc import ABC, abstractmethod
import json
import sqlite3

try:
    from .models import Pet
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
    )
except ImportError:
    from models import Pet
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
    )


class IConexaoDAO(ABC):
    """Interface para operações de conexão e execução no banco."""

    @abstractmethod
    def obter_conexao(self):
        pass

    @abstractmethod
    def executar_comando(self, comando, parametros=()):
        pass

    @abstractmethod
    def executar_select(self, comando, parametros=()):
        pass


class ConexaoBD(IConexaoDAO):
    """Executa operações SQLite, fechando a conexão após cada operação."""

    def __init__(self, caminho_banco: str = "db_solid.sqlite3"):
        self.caminho_banco = caminho_banco

    def obter_conexao(self) -> sqlite3.Connection:
        conexao = sqlite3.connect(self.caminho_banco)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON;")
        return conexao

    def executar_comando(self, comando, parametros=()):
        conexao = self.obter_conexao()
        try:
            cursor = conexao.execute(comando, parametros)
            conexao.commit()
            return cursor
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def executar_select(self, comando, parametros=()):
        conexao = self.obter_conexao()
        try:
            return conexao.execute(comando, parametros).fetchall()
        finally:
            conexao.close()


class ICrudDAO(ABC):
    """Interface usada para o CRUD das entidades."""

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
    _ENUMS = {
        "especie": EspecieEnum,
        "faixa_etaria": FaixaEtariaEnum,
        "cuidados": CuidadosEnum,
        "sexo": SexoAnimalEnum,
        "cond_esp": CondicoesEspecEnum,
        "porte": PorteEnum,
        "moradia": MoradiaEnum,
        "sociabilidade": SociabilidadeEnum,
        "alocacao": AlocacaoEnum,
        "comportamento": ComportamentoEnum,
    }

    _COLUNAS = (
        "nome, especie, faixa_etaria, cuidados, sexo, cond_esp, porte, "
        "moradia, sociabilidade, alocacao, comportamento, disponivel, "
        "fotos, biografia, data_nascimento"
    )

    def __init__(self, conexao_bd=None):
        self.conexao_bd = conexao_bd if conexao_bd is not None else ConexaoBD()

    @staticmethod
    def _valor_enum(valor):
        return valor.name if valor is not None else None

    @classmethod
    def _valores_pet(cls, pet):
        return (
            pet.nome,
            cls._valor_enum(pet.especie),
            cls._valor_enum(pet.faixa_etaria),
            cls._valor_enum(pet.cuidados),
            cls._valor_enum(pet.sexo),
            cls._valor_enum(pet.cond_esp),
            cls._valor_enum(pet.porte),
            cls._valor_enum(pet.moradia_recomendada),
            cls._valor_enum(pet.sociabilidade),
            cls._valor_enum(pet.alocacao),
            cls._valor_enum(pet.comportamento),
            int(pet.disponivel),
            json.dumps(pet.fotos, ensure_ascii=False),
            pet.biografia,
            pet.data_nascimento,
        )

    @classmethod
    def _pet_da_linha(cls, linha):
        if linha is None:
            return None

        dados = dict(linha)
        for campo, tipo_enum in cls._ENUMS.items():
            nome_enum = dados[campo]
            dados[campo] = tipo_enum[nome_enum] if nome_enum is not None else None

        dados["disponivel"] = bool(dados["disponivel"])
        dados["foto"] = json.loads(dados.pop("fotos"))
        return Pet(**dados)

    def criar(self, dados):
        if not isinstance(dados, Pet):
            raise TypeError("dados deve ser uma instância de Pet.")

        valores = self._valores_pet(dados)
        if dados.id is None:
            cursor = self.conexao_bd.executar_comando(
                f"INSERT INTO pets ({self._COLUNAS}) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                valores,
            )
            dados.id = cursor.lastrowid
        else:
            colunas = "id, " + self._COLUNAS
            marcadores = ", ".join("?" for _ in range(16))
            self.conexao_bd.executar_comando(
                f"INSERT INTO pets ({colunas}) VALUES ({marcadores})",
                (dados.id, *valores),
            )
        return dados

    def buscar_id(self, id):
        linhas = self.conexao_bd.executar_select(
            "SELECT * FROM pets WHERE id = ?", (id,)
        )
        return self._pet_da_linha(linhas[0]) if linhas else None

    def listar(self):
        linhas = self.conexao_bd.executar_select("SELECT * FROM pets ORDER BY id")
        return [self._pet_da_linha(linha) for linha in linhas]

    def alterar(self, id, novos_dados):
        if not isinstance(novos_dados, Pet):
            raise TypeError("novos_dados deve ser uma instância de Pet.")

        colunas = self._COLUNAS.split(", ")
        atribuicoes = ", ".join(f"{coluna} = ?" for coluna in colunas)
        cursor = self.conexao_bd.executar_comando(
            f"UPDATE pets SET {atribuicoes} WHERE id = ?",
            (*self._valores_pet(novos_dados), id),
        )
        if cursor.rowcount == 0:
            return None

        novos_dados.id = id
        return novos_dados

    def deletar(self, id):
        cursor = self.conexao_bd.executar_comando(
            "DELETE FROM pets WHERE id = ?", (id,)
        )
        return cursor.rowcount > 0
