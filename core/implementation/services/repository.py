from datetime import date

from core.implementation.services.models import Pet as PetModel, ONG as OngModel, Adotante as AdotanteModel
from core.domain.entities.dominio import Adotante, ONG, Pet
from core.domain.services.interfaces_dao import ICrudDAO
from core.domain.services.interfaces_repository import IRepository


class PetRepository(IRepository):
    def __init__(self, pet_dao: ICrudDAO):
        self.pet_dao = pet_dao

    def validar(self, pet: Pet) -> bool:
        if not isinstance(pet, Pet):
            raise TypeError("pet deve ser uma instância de Pet.")
        if not pet.nome or not pet.nome.strip():
            raise ValueError("O nome do animal não pode ficar em branco.")
        if pet.data_nascimento and pet.data_nascimento > date.today():
            raise ValueError("A data de nascimento não pode estar no futuro.")
        if pet.nome:
            pet.nome = pet.nome.strip()
        if pet.biografia:
            pet.biografia = pet.biografia.strip()
        return True

    def criar(self, pet: Pet) -> Pet:
        self.validar(pet)
        return self.pet_dao.criar(pet)

    def buscar_id(self, id: int) -> Pet | None:
        return self.pet_dao.buscar_id(id)

    def listar(self) -> list[Pet]:
        return self.pet_dao.listar()

    def alterar(self, id: int, pet: Pet) -> Pet | None:
        self.validar(pet)
        return self.pet_dao.alterar(id, pet)

    def deletar(self, id: int) -> bool:
        return self.pet_dao.deletar(id)


class OngRepository(IRepository):
    def __init__(self, ong_dao: ICrudDAO):
        self.ong_dao = ong_dao

    def validar(self, ong: ONG) -> bool:
        if not isinstance(ong, ONG):
            raise TypeError("ong deve ser uma instância de ONG.")
        if not ong.cnpj or not ong.cnpj.strip():
            raise ValueError("O CNPJ da ONG é obrigatório.")
        if not ong.razao_social or not ong.razao_social.strip():
            raise ValueError("A razão social da ONG é obrigatória.")
        ong.cnpj = "".join(char for char in ong.cnpj if char.isdigit())
        return True

    def criar(self, ong: ONG) -> ONG:
        self.validar(ong)
        return self.ong_dao.criar(ong)

    def buscar_id(self, id: int) -> ONG | None:
        return self.ong_dao.buscar_id(id)

    def listar(self) -> list[ONG]:
        return self.ong_dao.listar()

    def alterar(self, id: int, ong: ONG) -> ONG | None:
        self.validar(ong)
        return self.ong_dao.alterar(id, ong)

    def deletar(self, id: int) -> bool:
        return self.ong_dao.deletar(id)


class AdotanteRepository(IRepository):
    def __init__(self, adotante_dao: ICrudDAO):
        self.adotante_dao = adotante_dao

    def validar(self, adotante: Adotante) -> bool:
        if not isinstance(adotante, Adotante):
            raise TypeError("adotante deve ser uma instância de Adotante.")
        if adotante.data_nascimento:
            hoje = date.today()
            if adotante.data_nascimento > hoje:
                raise ValueError("A data de nascimento não pode estar no futuro.")
            idade = hoje.year - adotante.data_nascimento.year - (
                (hoje.month, hoje.day)
                < (adotante.data_nascimento.month, adotante.data_nascimento.day)
            )
            if idade < 18:
                raise ValueError("O adotante precisa ter pelo menos 18 anos.")
        if adotante.cpf:
            adotante.cpf = "".join(char for char in adotante.cpf if char.isdigit())
        return True

    def criar(self, adotante: Adotante) -> Adotante:
        self.validar(adotante)
        return self.adotante_dao.criar(adotante)

    def buscar_id(self, id: int) -> Adotante | None:
        return self.adotante_dao.buscar_id(id)

    def buscar_email(self, email: str) -> Adotante | None:
        return self.adotante_dao.buscar_email(email)

    def listar(self) -> list[Adotante]:
        return self.adotante_dao.listar()

    def alterar(self, id: int, adotante: Adotante) -> Adotante | None:
        self.validar(adotante)
        return self.adotante_dao.alterar(id, adotante)

    def deletar(self, id: int) -> bool:
        return self.adotante_dao.deletar(id)
