from django.db import connections, transaction
from django.conf import settings

from core.domain.entities.dominio import Adotante as AdotanteDomain
from core.domain.entities.dominio import ONG as ONGDomain
from core.domain.entities.dominio import Pet as PetDomain
from core.domain.entities.enums import (
    AlocacaoEnum,
    EspecieEnum,
    EstadoBrasileiroEnum,
    MoradiaEnum,
    PorteEnum,
    SexoAnimalEnum,
    TipoUsuarioEnum,
)
from core.domain.services.interfaces_dao import ICrudDAO
from core.implementation.services.models import (
    Adotante as AdotanteModel,
    ONG as ONGModel,
    Pet as PetModel,
    UsuarioBase,
)

def _enum_code(value):
    return value.codigo if value is not None else None


def _enum_from_code(enum_type, code):
    if code is None:
        return None
    return next((item for item in enum_type if item.codigo == code), None)


class ConexaoBD_ORM:
    DB_ALIAS = "default"

    def obter_conexao(self):
        if self.DB_ALIAS not in connections.databases:
            configuracao = connections.databases["default"].copy()
            configuracao.update(
                {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": settings.BASE_DIR / "db_solid.sqlite3",
                    "TIME_ZONE": "America/Fortaleza",
                    "CONN_MAX_AGE": 60,
                    "AUTOCOMMIT": True,
                    "ATOMIC_REQUESTS": False,
                }
            )
            connections.databases[self.DB_ALIAS] = configuracao
        return connections[self.DB_ALIAS]


class _BaseDAO:
    def __init__(self, conexao: ConexaoBD_ORM | None = None):
        self._conexao = conexao or ConexaoBD_ORM()
        self._conexao.obter_conexao()
        self._db = self._conexao.DB_ALIAS

    @staticmethod
    def _usuario_para_dominio(usuario: UsuarioBase) -> dict:
        return {
            "id": usuario.pk,
            "email": usuario.email,
            "senha": usuario.password,
            "cep": usuario.cep,
            "rua": usuario.rua,
            "numero": usuario.numero,
            "bairro": usuario.bairro,
            "cidade": usuario.cidade,
            "estado": _enum_from_code(EstadoBrasileiroEnum, usuario.estado),
            "telefone": usuario.telefone,
            "url_foto_perfil": usuario.foto_perfil.name or None,
        }

    def _salvar_usuario(self, dados, usuario: UsuarioBase | None = None):
        usuario = usuario or UsuarioBase()
        usuario.username = dados.email
        usuario.email = dados.email
        if hasattr(dados, "nome"):
            usuario.first_name = dados.nome or ""
        usuario.cep = dados.cep
        usuario.rua = dados.rua
        usuario.numero = dados.numero
        usuario.bairro = dados.bairro
        usuario.cidade = dados.cidade
        usuario.estado = _enum_code(dados.estado)
        usuario.telefone = dados.telefone
        usuario.foto_perfil = dados.url_foto_perfil or ""
        if dados.senha:
            usuario.set_password(dados.senha)
        elif usuario.pk is None:
            raise ValueError("A senha é obrigatória para criar o usuário.")
        usuario.full_clean()
        usuario.save(using=self._db)
        return usuario


class PetDAO_ORM(_BaseDAO, ICrudDAO):
    @staticmethod
    def _para_modelo(dados: PetDomain, ong: ONGModel) -> PetModel:
        return PetModel(
            ong=ong,
            especie=_enum_code(dados.especie),
            nome=dados.nome,
            sexo=_enum_code(dados.sexo),
            data_nascimento=dados.data_nascimento,
            alocacao=_enum_code(dados.alocacao),
            porte=_enum_code(dados.porte),
            moradia_recomendada=_enum_code(dados.moradia_recomendada),
            disponivel=dados.disponivel,
            biografia=dados.biografia,
        )

    @staticmethod
    def _para_dominio(registro: PetModel) -> PetDomain:
        ong = OngDAO_ORM._para_dominio(registro.ong, incluir_pets=False)
        return PetDomain(
            id=registro.pk,
            nome=registro.nome,
            especie=_enum_from_code(EspecieEnum, registro.especie),
            ong=ong,
            sexo=_enum_from_code(SexoAnimalEnum, registro.sexo),
            porte=_enum_from_code(PorteEnum, registro.porte),
            moradia=_enum_from_code(MoradiaEnum, registro.moradia_recomendada),
            alocacao=_enum_from_code(AlocacaoEnum, registro.alocacao),
            disponivel=registro.disponivel,
            biografia=registro.biografia,
            data_nascimento=registro.data_nascimento,
        )

    def criar(self, dados: PetDomain) -> PetDomain:
        if not isinstance(dados, PetDomain):
            raise TypeError("dados deve ser uma instância de Pet.")
        if not isinstance(dados.ong, ONGDomain) or dados.ong.id is None:
            raise ValueError("Pet deve estar associado a uma ONG persistida.")

        ong = ONGModel.objects.using(self._db).get(pk=dados.ong.id)
        registro = self._para_modelo(dados, ong)
        registro.full_clean()
        registro.save(using=self._db)
        dados.id = registro.pk
        return dados

    def buscar_id(self, id: int) -> PetDomain | None:
        registro = PetModel.objects.using(self._db).filter(pk=id).first()
        return self._para_dominio(registro) if registro else None

    def listar(self) -> list[PetDomain]:
        registros = PetModel.objects.using(self._db).select_related("ong").order_by("pk")
        return [self._para_dominio(registro) for registro in registros]

    def alterar(self, id: int, novos_dados: PetDomain) -> PetDomain | None:
        if not isinstance(novos_dados, PetDomain):
            raise TypeError("novos_dados deve ser uma instância de Pet.")

        registro = PetModel.objects.using(self._db).filter(pk=id).first()
        if registro is None:
            return None

        if not isinstance(novos_dados.ong, ONGDomain) or novos_dados.ong.id is None:
            raise ValueError("Pet deve estar associado a uma ONG persistida.")
        ong = ONGModel.objects.using(self._db).get(pk=novos_dados.ong.id)
        atualizado = self._para_modelo(novos_dados, ong)
        atualizado.pk = registro.pk
        atualizado.full_clean(exclude=["id"])
        atualizado.save(using=self._db)
        novos_dados.id = atualizado.pk
        return novos_dados

    def deletar(self, id: int) -> bool:
        removidos, _ = PetModel.objects.using(self._db).filter(pk=id).delete()
        return removidos > 0


class OngDAO_ORM(_BaseDAO, ICrudDAO):
    @staticmethod
    def _para_dominio(
        registro: ONGModel, incluir_pets: bool = True
    ) -> ONGDomain:
        usuario = registro.ong
        dados = _BaseDAO._usuario_para_dominio(usuario)
        dados.update(
            cnpj=registro.cnpj,
            razao_social=registro.razao_social,
            descricao=registro.descricao,
            pix_para_doacao=registro.pix_doacao,
        )
        ong = ONGDomain(**dados)
        if incluir_pets:
            ong.pets = [
                PetDAO_ORM._para_dominio(pet)
                for pet in registro.pets_mantidos.all()
            ]
        return ong

    def criar(self, dados: ONGDomain) -> ONGDomain:
        if not isinstance(dados, ONGDomain):
            raise TypeError("dados deve ser uma instância de ONG.")

        with transaction.atomic(using=self._db):
            usuario = self._salvar_usuario(dados)
            usuario.tipo_usuario = TipoUsuarioEnum.ONG.codigo
            usuario.save(using=self._db, update_fields=["tipo_usuario"])
            registro = ONGModel(
                ong=usuario,
                cnpj=dados.cnpj,
                razao_social=dados.razao_social,
                descricao=dados.descricao,
                pix_doacao=dados.pix_para_doacao,
            )
            registro.full_clean()
            registro.save(using=self._db)
            dados.id = usuario.pk
            for pet in dados.pets:
                pet_model = PetDAO_ORM._para_modelo(pet, registro)
                pet_model.full_clean()
                pet_model.save(using=self._db)
                pet.id = pet_model.pk
        return dados

    def buscar_id(self, id: int) -> ONGDomain | None:
        registro = (
            ONGModel.objects.using(self._db)
            .select_related("ong")
            .prefetch_related("pets_mantidos")
            .filter(ong_id=id)
            .first()
        )
        return self._para_dominio(registro) if registro else None

    def listar(self) -> list[ONGDomain]:
        registros = (
            ONGModel.objects.using(self._db)
            .select_related("ong")
            .prefetch_related("pets_mantidos")
            .order_by("ong_id")
        )
        return [self._para_dominio(registro) for registro in registros]

    def alterar(self, id: int, novos_dados: ONGDomain) -> ONGDomain | None:
        if not isinstance(novos_dados, ONGDomain):
            raise TypeError("novos_dados deve ser uma instância de ONG.")

        registro = (
            ONGModel.objects.using(self._db)
            .select_related("ong")
            .filter(ong_id=id)
            .first()
        )
        if registro is None:
            return None

        with transaction.atomic(using=self._db):
            usuario = self._salvar_usuario(novos_dados, registro.ong)
            usuario.tipo_usuario = TipoUsuarioEnum.ONG.codigo
            usuario.save(using=self._db, update_fields=["tipo_usuario"])
            registro.cnpj = novos_dados.cnpj
            registro.razao_social = novos_dados.razao_social
            registro.descricao = novos_dados.descricao
            registro.pix_doacao = novos_dados.pix_para_doacao
            registro.full_clean()
            registro.save(using=self._db)
        novos_dados.id = usuario.pk
        return novos_dados

    def deletar(self, id: int) -> bool:
        registro = ONGModel.objects.using(self._db).filter(ong_id=id).first()
        if registro is None:
            return False
        registro.ong.delete(using=self._db)
        return True


class AdotanteDAO_ORM(_BaseDAO, ICrudDAO):
    @staticmethod
    def _para_dominio(registro: AdotanteModel) -> AdotanteDomain:
        dados = _BaseDAO._usuario_para_dominio(registro.adotante)
        dados.update(
            nome=registro.nome,
            cpf=registro.cpf,
            data_nascimento=registro.data_nascimento,
        )
        return AdotanteDomain(**dados)

    def criar(self, dados: AdotanteDomain) -> AdotanteDomain:
        if not isinstance(dados, AdotanteDomain):
            raise TypeError("dados deve ser uma instância de Adotante.")

        with transaction.atomic(using=self._db):
            usuario = self._salvar_usuario(dados)
            usuario.tipo_usuario = TipoUsuarioEnum.ADOTANTE.codigo
            usuario.save(using=self._db, update_fields=["tipo_usuario"])
            registro = AdotanteModel(
                adotante=usuario,
                nome=getattr(dados, "nome", None),
                cpf=dados.cpf,
                data_nascimento=dados.data_nascimento,
            )
            registro.full_clean()
            registro.save(using=self._db)
            dados.id = usuario.pk
        return dados

    def buscar_id(self, id: int) -> AdotanteDomain | None:
        registro = (
            AdotanteModel.objects.using(self._db)
            .select_related("adotante")
            .filter(adotante_id=id)
            .first()
        )
        return self._para_dominio(registro) if registro else None

    def buscar_email(self, email: str) -> AdotanteDomain | None:
        registro = (
            AdotanteModel.objects.using(self._db)
            .select_related("adotante")
            .filter(adotante__email__iexact=email)
            .first()
        )
        return self._para_dominio(registro) if registro else None

    def listar(self) -> list[AdotanteDomain]:
        registros = (
            AdotanteModel.objects.using(self._db)
            .select_related("adotante")
            .order_by("adotante_id")
        )
        return [self._para_dominio(registro) for registro in registros]

    def alterar(self, id: int, novos_dados: AdotanteDomain) -> AdotanteDomain | None:
        if not isinstance(novos_dados, AdotanteDomain):
            raise TypeError("novos_dados deve ser uma instância de Adotante.")

        registro = (
            AdotanteModel.objects.using(self._db)
            .select_related("adotante")
            .filter(adotante_id=id)
            .first()
        )
        if registro is None:
            return None

        with transaction.atomic(using=self._db):
            usuario = self._salvar_usuario(novos_dados, registro.adotante)
            usuario.tipo_usuario = TipoUsuarioEnum.ADOTANTE.codigo
            usuario.save(using=self._db, update_fields=["tipo_usuario"])
            registro.nome = getattr(novos_dados, "nome", None)
            registro.cpf = novos_dados.cpf
            registro.data_nascimento = novos_dados.data_nascimento
            registro.full_clean()
            registro.save(using=self._db)
        novos_dados.id = usuario.pk
        return novos_dados

    def deletar(self, id: int) -> bool:
        registro = AdotanteModel.objects.using(self._db).filter(adotante_id=id).first()
        if registro is None:
            return False
        registro.adotante.delete(using=self._db)
        return True