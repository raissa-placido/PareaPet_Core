from core.domain.entities.dominio import Adotante
from core.domain.services.interfaces_repository import IRepository


class AdotanteService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def listar(self) -> list[Adotante]:
        return self.repository.listar()

    def obter_por_id(self, id: int) -> Adotante:
        adotante = self.repository.buscar_id(id)
        if adotante is None:
            raise LookupError(f"Adotante com id={id} não encontrado.")
        return adotante

    def obter_por_email(self, email: str) -> Adotante | None:
        return self.repository.buscar_email(email)

    def incluir(self, adotante: Adotante) -> Adotante:
        return self.repository.criar(adotante)

    def alterar(self, adotante: Adotante) -> Adotante:
        if adotante.id is None:
            raise ValueError("O id do adotante é obrigatório para alteração.")
        atualizado = self.repository.alterar(adotante.id, adotante)
        if atualizado is None:
            raise LookupError(f"Adotante com id={adotante.id} não encontrado.")
        return atualizado

    def excluir(self, id: int) -> None:
        if not self.repository.deletar(id):
            raise LookupError(f"Adotante com id={id} não encontrado.")
