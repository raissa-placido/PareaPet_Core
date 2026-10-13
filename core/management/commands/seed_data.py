from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from core.domain.entities.enums import (
    AlocacaoEnum,
    EspecieEnum,
    MoradiaEnum,
    PorteEnum,
    SexoAnimalEnum,
    TipoUsuarioEnum,
)
from core.implementation.services.models import ONG, Pet, UsuarioBase


ONGS = (
    {
        "username": "ong_amigos_dos_animais",
        "email": "contato@amigosdosanimais.org",
        "cnpj": "04252011000110",
        "razao_social": "ONG Amigos dos Animais",
        "descricao": "Resgate e cuidado de animais abandonados.",
        "pix_doacao": "doe@amigosdosanimais.org",
    },
    {
        "username": "ong_patas_felizes",
        "email": "contato@patasfelizes.org",
        "cnpj": "45723174000110",
        "razao_social": "ONG Patas Felizes",
        "descricao": "Acolhimento e adoção responsável de cães e gatos.",
        "pix_doacao": "doe@patasfelizes.org",
    },
    {
        "username": "ong_vida_animal",
        "email": "contato@vidaanimal.org",
        "cnpj": "11222333000181",
        "razao_social": "ONG Vida Animal",
        "descricao": "Proteção, tratamento e encaminhamento para adoção.",
        "pix_doacao": "doe@vidaanimal.org",
    },
)

PETS = (
    {
        "nome": "Luna",
        "especie": EspecieEnum.GATO.codigo,
        "sexo": SexoAnimalEnum.FEMEA.codigo,
        "data_nascimento": date(2022, 4, 12),
        "alocacao": AlocacaoEnum.NA_ONG.codigo,
        "porte": PorteEnum.PEQUENO.codigo,
        "moradia_recomendada": MoradiaEnum.APARTAMENTO.codigo,
        "biografia": "Gata dócil e carinhosa.",
        "ong_index": 0,
    },
    {
        "nome": "Thor",
        "especie": EspecieEnum.CACHORRO.codigo,
        "sexo": SexoAnimalEnum.MACHO.codigo,
        "data_nascimento": date(2021, 8, 3),
        "alocacao": AlocacaoEnum.NA_ONG.codigo,
        "porte": PorteEnum.GRANDE.codigo,
        "moradia_recomendada": MoradiaEnum.CASA.codigo,
        "biografia": "Cachorro brincalhão e protetor.",
        "ong_index": 0,
    },
    {
        "nome": "Mel",
        "especie": EspecieEnum.CACHORRO.codigo,
        "sexo": SexoAnimalEnum.FEMEA.codigo,
        "data_nascimento": date(2023, 1, 20),
        "alocacao": AlocacaoEnum.NO_LAR_TEMPORARIO.codigo,
        "porte": PorteEnum.MEDIO.codigo,
        "moradia_recomendada": MoradiaEnum.CASA.codigo,
        "biografia": "Muito sociável e cuidadosa com crianças.",
        "ong_index": 1,
    },
    {
        "nome": "Bento",
        "especie": EspecieEnum.CACHORRO.codigo,
        "sexo": SexoAnimalEnum.MACHO.codigo,
        "data_nascimento": date(2020, 11, 7),
        "alocacao": AlocacaoEnum.NA_ONG.codigo,
        "porte": PorteEnum.MEDIO.codigo,
        "moradia_recomendada": MoradiaEnum.CASA.codigo,
        "biografia": "Companheiro, tranquilo e obediente.",
        "ong_index": 1,
    },
    {
        "nome": "Nina",
        "especie": EspecieEnum.GATO.codigo,
        "sexo": SexoAnimalEnum.FEMEA.codigo,
        "data_nascimento": date(2024, 2, 15),
        "alocacao": AlocacaoEnum.NA_ONG.codigo,
        "porte": PorteEnum.PEQUENO.codigo,
        "moradia_recomendada": MoradiaEnum.APARTAMENTO.codigo,
        "biografia": "Filhote curiosa e afetuosa.",
        "ong_index": 2,
    },
)


class Command(BaseCommand):
    help = "Cria dados fictícios para desenvolvimento: 3 ONGs e 5 pets."

    def handle(self, *args, **options):
        with transaction.atomic(using="db_solid"):
            ongs = [self._create_ong(data) for data in ONGS]
            for pet_data in PETS:
                self._create_pet(pet_data, ongs[pet_data["ong_index"]])

        self.stdout.write(
            self.style.SUCCESS("Seed concluído: 3 ONGs e 5 pets disponíveis.")
        )

    @staticmethod
    def _create_ong(data):
        usuario, _ = UsuarioBase.objects.using("db_solid").get_or_create(
            username=data["username"],
            defaults={
                "email": data["email"],
                "tipo_usuario": TipoUsuarioEnum.ONG.codigo,
            },
        )
        usuario.email = data["email"]
        usuario.tipo_usuario = TipoUsuarioEnum.ONG.codigo
        usuario.set_unusable_password()
        usuario.full_clean()
        usuario.save(using="db_solid")

        ong, _ = ONG.objects.using("db_solid").get_or_create(
            ong=usuario,
            defaults={
                "cnpj": data["cnpj"],
                "razao_social": data["razao_social"],
                "descricao": data["descricao"],
                "pix_doacao": data["pix_doacao"],
            },
        )
        ong.cnpj = data["cnpj"]
        ong.razao_social = data["razao_social"]
        ong.descricao = data["descricao"]
        ong.pix_doacao = data["pix_doacao"]
        ong.full_clean()
        ong.save(using="db_solid")
        return ong

    @staticmethod
    def _create_pet(data, ong):
        pet_data = {
            key: value for key, value in data.items() if key != "ong_index"
        }
        pet, _ = Pet.objects.using("db_solid").get_or_create(
            ong=ong,
            nome=data["nome"],
            defaults=pet_data,
        )
        for key, value in pet_data.items():
            setattr(pet, key, value)
        pet.ong = ong
        pet.disponivel = True
        pet.full_clean()
        pet.save(using="db_solid")
        return pet