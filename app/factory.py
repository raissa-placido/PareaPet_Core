from core.implementation.services.dao import (
    AdotanteDAO_ORM,
    ConexaoBD_ORM,
    OngDAO_ORM,
    PetDAO_ORM,
)
from core.implementation.services.repository import (
    AdotanteRepository,
    OngRepository,
    PetRepository,
)


class ServicosFactory:

    def obter_conexao_bd(self):
        return ConexaoBD_ORM()

    def obter_pet_dao(self):
        return PetDAO_ORM(self.obter_conexao_bd())

    def obter_ong_dao(self):
        return OngDAO_ORM(self.obter_conexao_bd())

    def obter_adotante_dao(self):
        return AdotanteDAO_ORM(self.obter_conexao_bd())

    def obter_pet_repository(self):
        return PetRepository(self.obter_pet_dao())

    def obter_ong_repository(self):
        return OngRepository(self.obter_ong_dao())

    def obter_adotante_repository(self):
        return AdotanteRepository(self.obter_adotante_dao())
