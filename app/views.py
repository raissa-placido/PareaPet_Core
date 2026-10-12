from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from app.factory import ServicosFactory
from app.forms import OngForm
from core.domain.entities.dominio import ONG
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


def home(request):
    return render(request, "home.html")


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
        except (ValidationError, ValueError, TypeError) as error:
            _add_repository_error(form, error)

    return render(request, "ongs/formulario.html", {"form": form, "titulo": "Cadastrar ONG"})


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
        except (ValidationError, ValueError, TypeError) as error:
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
