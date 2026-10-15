from django.urls import path

from app import views


app_name = "usuario_pp"

urlpatterns = [
    path("cadastro/adotante/", views.pre_cadastro_adotante, name="PreCadastro"),
    path(
        "cadastro/adotante/completar/",
        views.cadastro_adotante,
        name="cadastro_adotante",
    ),
    path(
        "cadastro/adotante/questionario/",
        views.questionario_adotante,
        name="questionario_adotante",
    ),
    path("login/", views.login_adotante, name="login"),
    path("logout/", views.logout_adotante, name="logout"),
    path("perfil/", views.perfil_usuario, name="perfil_usuario"),
    path(
        "perfil/alterar/",
        views.alterar_cadastro_adotante,
        name="alterar_cadastro",
    ),
    path(
        "perfil/excluir/",
        views.excluir_adotante,
        name="excluir_adotante",
    ),
    path("perfil/adocoes/", views.status_adocao, name="status_adocao"),
]
