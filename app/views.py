from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

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


##### PET ####
##### PET ####
##### PET ####

def _pet_repository():
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
            {"registros": _pet_repository().listar(), "ERRO": "Método inválido."},
            status=405,
        )
    return render(
        request,
        "pets_listar.html",
        {"registros": _pet_repository().listar()},
    )


def adicionar_pet(request):
    form = PetForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            _pet_repository().criar(_pet_from_form(form))
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
    repository = _pet_repository()
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
    repository = _pet_repository()
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


### ONG ###
### ONG ###
### ONG ###

def home(request):
    return HttpResponseRedirect(reverse("listar_pets"))
from app.forms import AdotanteForm, OngForm
from core.domain.entities.dominio import Adotante, ONG
from core.domain.entities.enums import EstadoBrasileiroEnum


def _repository():
    return ServicosFactory().obter_ong_repository()


def _ong_from_form(form, ong_id=None, ong_atual=None):
    dados = form.cleaned_data
    estado_codigo = dados["estado"]
    estado = (
        next(
            item
            for item in EstadoBrasileiroEnum
            if item.codigo == int(estado_codigo)
        )
        if estado_codigo
        else None
    )
    return ONG(
        id=ong_id,
        cnpj=dados["cnpj"],
        razao_social=dados["razao_social"],
        descricao=dados["descricao"],
        pix_para_doacao=dados["pix_para_doacao"],
        email=dados["email"],
        senha=dados["senha"],
        cep=dados["cep"],
        rua=dados["rua"],
        numero=dados["numero"],
        bairro=dados["bairro"],
        cidade=dados["cidade"],
        estado=estado,
        telefone=dados["telefone"],
        url_foto_perfil=ong_atual.url_foto_perfil if ong_atual else None,
    )


def _add_repository_error(form, error):
    if isinstance(error, ValidationError):
        message = "; ".join(str(item) for item in error.messages)
    else:
        message = str(error)
    form.add_error(None, message)


### ADOTANTE ###
### ADOTANTE ###
### ADOTANTE ###

def home(request):
    return render(request, "adotante/inicio.html")


def listar_ongs(request):
    ongs = _repository().listar()
    return render(request, "ongs/listar.html", {"ongs": ongs})


def detalhe_ong(request, ong_id):
    ong = _repository().buscar_id(ong_id)
    if ong is None:
        return render(request, "404.html", status=404)
    return render(request, "ongs/detalhe.html", {"ong": ong})


@require_http_methods(["GET", "POST"])
def criar_ong(request):
    form = OngForm(request.POST or None, criar=True)
    if request.method == "POST" and form.is_valid():
        try:
            _repository().criar(_ong_from_form(form))
            messages.success(request, "ONG cadastrada com sucesso.")
            return redirect("ongs_listar")
        except (ValidationError, ValueError, TypeError, IntegrityError) as error:
            _add_repository_error(form, error)

    return render(
        request,
        "ongs/formulario.html",
        {"form": form, "titulo": "Cadastrar ONG"},
    )


@require_http_methods(["GET", "POST"])
def editar_ong(request, ong_id):
    repository = _repository()
    ong = repository.buscar_id(ong_id)
    if ong is None:
        return render(request, "404.html", status=404)

    form = OngForm(request.POST or None, ong=ong)
    if request.method == "POST" and form.is_valid():
        try:
            atualizado = _ong_from_form(form, ong_id=ong_id, ong_atual=ong)
            resultado = repository.alterar(ong_id, atualizado)
            if resultado is None:
                return render(request, "404.html", status=404)
            messages.success(request, "Dados da ONG atualizados com sucesso.")
            return redirect("ongs_detalhe", ong_id=ong_id)
        except (ValidationError, ValueError, TypeError, IntegrityError) as error:
            _add_repository_error(form, error)

    return render(
        request,
        "ongs/formulario.html",
        {"form": form, "titulo": "Editar ONG", "ong": ong},
    )


@require_http_methods(["GET", "POST"])
def excluir_ong(request, ong_id):
    repository = _repository()
    ong = repository.buscar_id(ong_id)
    if ong is None:
        return render(request, "404.html", status=404)

    if request.method == "POST":
        try:
            if repository.deletar(ong_id):
                messages.success(request, "ONG excluída com sucesso.")
                return redirect("ongs_listar")
            return render(request, "404.html", status=404)
        except ProtectedError:
            messages.error(
                request,
                "Esta ONG não pode ser excluída enquanto possuir animais cadastrados.",
            )
            return redirect("ongs_detalhe", ong_id=ong_id)
        except (ValidationError, ValueError, TypeError) as error:
            messages.error(request, str(error))
            return redirect("ongs_detalhe", ong_id=ong_id)

    return render(request, "ongs/confirmar_exclusao.html", {"ong": ong})


### ADOTANTE ###
### ADOTANTE ###
### ADOTANTE ###

def _obter_adotante_da_sessao(request):
    adotante_id = request.session.get("adotante_id")
    if adotante_id is None:
        return None
    try:
        return ServicosFactory().obter_adotante_service().obter_por_id(
            int(adotante_id)
        )
    except (TypeError, ValueError, LookupError):
        request.session.pop("adotante_id", None)
        return None


def pre_cadastro_adotante(request):
    if request.method == "GET":
        if _obter_adotante_da_sessao(request) is not None:
            return HttpResponseRedirect(reverse("usuario_pp:cadastro_adotante"))
        return render(request, "adotante/cadastro.html")
    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    nome = request.POST.get("nome", "").strip()
    email = request.POST.get("email", "").strip().lower()
    senha = request.POST.get("senha", "")
    confirmar_senha = request.POST.get("confirmarSenha", "")
    if not nome or not email or not senha:
        erro = "Preencha nome, e-mail e senha."
    elif senha != confirmar_senha:
        erro = "As senhas não conferem."
    else:
        adotante = Adotante(
            id=None,
            nome=nome,
            cpf=None,
            data_nascimento=None,
            email=email,
            senha=senha,
            cep=None,
            rua=None,
            numero=None,
            bairro=None,
            cidade=None,
            estado=None,
            telefone=None,
        )
        try:
            criado = ServicosFactory().obter_adotante_service().incluir(adotante)
            request.session["adotante_id"] = criado.id
            request.session.pop("adotante_questionario", None)
            return HttpResponseRedirect(reverse("usuario_pp:cadastro_adotante"))
        except (ValidationError, ValueError, IntegrityError) as error:
            erro = str(error)

    return render(request, "adotante/cadastro.html", {"erro": erro})


def cadastro_adotante(request):
    adotante = _obter_adotante_da_sessao(request)
    if adotante is None:
        return HttpResponseRedirect(reverse("usuario_pp:PreCadastro"))
    estados = list(EstadoBrasileiroEnum)
    if request.method == "GET":
        return render(
            request,
            "adotante/completar.html",
            {"adotante": adotante, "estados": estados},
        )
    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    form_data = request.POST.copy()
    form_data.update(
        {
            "id": str(adotante.id),
            "nome": adotante.nome or "",
            "email": adotante.email or "",
            "senha": "",
        }
    )
    form = AdotanteForm(form_data, is_update=True)
    if not form.is_valid():
        return render(
            request,
            "adotante/completar.html",
            {"adotante": adotante, "estados": estados, "erro": form.errors},
        )

    dados = form.cleaned_data
    dados["email"] = dados["email"].strip().lower()
    dados["cpf"] = dados["cpf"] or None
    dados["estado"] = next(
        (
            estado
            for estado in EstadoBrasileiroEnum
            if str(estado.codigo) == dados["estado"]
        ),
        None,
    )
    try:
        ServicosFactory().obter_adotante_service().alterar(Adotante(**dados))
        return HttpResponseRedirect(reverse("usuario_pp:questionario_adotante"))
    except (ValidationError, ValueError, LookupError, IntegrityError) as error:
        return render(
            request,
            "adotante/completar.html",
            {"adotante": adotante, "estados": estados, "erro": str(error)},
        )


def questionario_adotante(request):
    if _obter_adotante_da_sessao(request) is None:
        return HttpResponseRedirect(reverse("usuario_pp:PreCadastro"))
    if request.method == "POST":
        respostas = {
            chave: request.POST.getlist(chave)
            for chave in request.POST
            if chave.startswith("q")
        }
        request.session["adotante_questionario"] = respostas
        return HttpResponseRedirect(reverse("usuario_pp:perfil_usuario"))
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET", "POST"])
    return render(request, "adotante/questionario.html")


def perfil_usuario(request):
    adotante = _obter_adotante_da_sessao(request)
    if adotante is None:
        return HttpResponseRedirect(reverse("usuario_pp:login"))
    return render(
        request,
        "adotante/perfil.html",
        {
            "adotante": adotante,
            "respostas_questionario": request.session.get(
                "adotante_questionario", {}
            ),
        },
    )


def alterar_cadastro_adotante(request):
    adotante = _obter_adotante_da_sessao(request)
    if adotante is None:
        return HttpResponseRedirect(reverse("usuario_pp:login"))
    estados = [
        (estado.codigo, estado.descricao) for estado in EstadoBrasileiroEnum
    ]
    if request.method == "GET":
        return render(
            request,
            "adotante/alterar.html",
            {"adotante": adotante, "estados": estados},
        )
    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    dados_formulario = request.POST.copy()
    dados_formulario["id"] = str(adotante.id)
    dados_formulario.setdefault("nome", adotante.nome or "")
    dados_formulario.setdefault("email", adotante.email or "")
    dados_formulario.setdefault("senha", "")
    if "sem_numero" in dados_formulario and not dados_formulario.get("numero"):
        dados_formulario["numero"] = "S/N"
    form = AdotanteForm(dados_formulario, is_update=True)
    if not form.is_valid():
        return render(
            request,
            "adotante/alterar.html",
            {"adotante": adotante, "estados": estados, "erro": form.errors},
        )

    dados = form.cleaned_data
    dados["email"] = dados["email"].strip().lower()
    dados["cpf"] = dados["cpf"] or None
    dados["estado"] = next(
        (
            estado
            for estado in EstadoBrasileiroEnum
            if str(estado.codigo) == dados["estado"]
        ),
        None,
    )
    try:
        ServicosFactory().obter_adotante_service().alterar(Adotante(**dados))
        return HttpResponseRedirect(reverse("usuario_pp:perfil_usuario"))
    except (ValidationError, ValueError, LookupError, IntegrityError) as error:
        return render(
            request,
            "adotante/alterar.html",
            {"adotante": adotante, "estados": estados, "erro": str(error)},
        )


def excluir_adotante(request):
    adotante = _obter_adotante_da_sessao(request)
    if adotante is None:
        return HttpResponseRedirect(reverse("usuario_pp:login"))
    if request.method == "GET":
        return render(request, "adotante/excluir.html", {"adotante": adotante})
    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    try:
        ServicosFactory().obter_adotante_service().excluir(adotante.id)
    except LookupError:
        request.session.flush()
        return HttpResponseRedirect(reverse("home"))
    request.session.flush()
    return HttpResponseRedirect(reverse("home"))


def login_adotante(request):
    if _obter_adotante_da_sessao(request) is not None:
        return HttpResponseRedirect(reverse("usuario_pp:perfil_usuario"))
    if request.method == "GET":
        return render(request, "adotante/login.html")
    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    email = request.POST.get("email", "").strip().lower()
    senha = request.POST.get("senha", "")
    servico = ServicosFactory().obter_adotante_service()
    adotante = servico.obter_por_email(email) if email else None
    if adotante is None or not check_password(senha, adotante.senha):
        return render(
            request,
            "adotante/login.html",
            {"erro": "E-mail ou senha inválidos."},
        )
    request.session["adotante_id"] = adotante.id
    return HttpResponseRedirect(reverse("usuario_pp:perfil_usuario"))


def logout_adotante(request):
    request.session.flush()
    return HttpResponseRedirect(reverse("home"))


def status_adocao(request):
    if _obter_adotante_da_sessao(request) is None:
        return HttpResponseRedirect(reverse("usuario_pp:login"))
    return HttpResponseRedirect(reverse("usuario_pp:perfil_usuario"))
