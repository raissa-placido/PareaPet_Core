from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.factory import ServicosFactory
from app.forms import PetForm
from core.domain.entities.dominio import Pet
from core.domain.entities.enums import (
    AlocacaoEnum,
    EspecieEnum,
    MoradiaEnum,
    PorteEnum,
    SexoAnimalEnum,
)


def _repository():
    return ServicosFactory().obter_pet_repository()

# retorna a enumeração equivalente ao código informado
def _enum_by_code(enum_class, code):
    return next(item for item in enum_class if item.codigo == code)

# retorna um pet
def _pet_from_form(form, pet_id=None):
    data = form.cleaned_data
    ong = ServicosFactory().obter_ong_repository().buscar_id(data["ong"].ong_id)
    if ong is None:
        raise ValueError("A ONG selecionada não foi encontrada.")

    return Pet(
        id=pet_id,
        nome=data["nome"],
        especie=_enum_by_code(EspecieEnum, data["especie"]),
        ong=ong,
        sexo=_enum_by_code(SexoAnimalEnum, data["sexo"]),
        porte=_enum_by_code(PorteEnum, data["porte"]),
        moradia=_enum_by_code(MoradiaEnum, data["moradia_recomendada"]),
        alocacao=_enum_by_code(AlocacaoEnum, data["alocacao"]),
        disponivel=data["disponivel"],
        biografia=data["biografia"],
        data_nascimento=data["data_nascimento"],
    )

# retorna uma um formulário de pet
def _form_from_pet(pet):
    return PetForm(
        initial={
            "ong": pet.ong.id,
            "especie": pet.especie.codigo,
            "sexo": pet.sexo.codigo,
            "nome": pet.nome,
            "data_nascimento": pet.data_nascimento,
            "alocacao": pet.alocacao.codigo,
            "porte": pet.porte.codigo,
            "moradia_recomendada": pet.moradia_recomendada.codigo,
            "disponivel": pet.disponivel,
            "biografia": pet.biografia,
        }
    )


def listar_pets(request):
    if request.method != "GET":
        return render(
            request,
            "pets_listar.html",
            {"registros": _repository().listar(), "ERRO": "Método inválido."},
            status=405,
        )
    return render(
        request,
        "pets_listar.html",
        {"registros": _repository().listar()},
    )


def adicionar_pet(request):
    form = PetForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            _repository().criar(_pet_from_form(form))
            return HttpResponseRedirect(reverse("listar_pets"))
        except (TypeError, ValueError, ValidationError) as error:
            form.add_error(None, str(error))

    return render(
        request,
        "pets_editar.html",
        {
            "acao": "Inclusão",
            "form": form,
        },
    )


def alterar_pet(request, id):

    # busca do pet
    repository = _repository()
    pet = repository.buscar_id(id)
    if pet is None:
        return render(
            request,
            "pets_listar.html",
            {
                "registros": repository.listar(),
                "ERRO": "Pet não encontrado.",
            },
            status=404,
        )


    form = (
        PetForm(request.POST)
        if request.method == "POST"
        else _form_from_pet(pet)
    )
    
    if request.method == "POST" and form.is_valid():
        try:
            if repository.alterar(id, _pet_from_form(form, id)) is None:
                raise ValueError("Pet não encontrado.")
            return HttpResponseRedirect(reverse("listar_pets"))
        except (TypeError, ValueError, ValidationError) as error:
            form.add_error(None, str(error))

    return render(
        request,
        "pets_editar.html",
        {
            "acao": "Alteração",
            "form": form,
            "pet_id": id,
        },
    )


def remover_pet(request, id):
    repository = _repository()
    pet = repository.buscar_id(id)
    if pet is None:
        return render(
            request,
            "pets_listar.html",
            {
                "registros": repository.listar(),
                "ERRO": "Pet não encontrado.",
            },
            status=404,
        )

    if request.method == "POST":
        try:
            if not repository.deletar(id):
                raise ValueError("Pet não encontrado.")
            return HttpResponseRedirect(reverse("listar_pets"))
        except (TypeError, ValueError, ValidationError) as error:
            return render(
                request,
                "pets_remover.html",
                {"pet": pet, "ERRO": str(error)},
                status=400,
            )

    return render(request, "pets_remover.html", {"pet": pet})


def home(request):
    return HttpResponseRedirect(reverse("listar_pets"))