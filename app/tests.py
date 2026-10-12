from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from app.forms import OngForm
from core.domain.entities.enums import EstadoBrasileiroEnum
from core.implementation.services.dao import ConexaoBD_ORM


class OngFormTests(SimpleTestCase):
    def test_cadastro_exige_senha(self):
        form = OngForm(
            data={
                "cnpj": "11.222.333/0001-81",
                "razao_social": "ONG Exemplo",
                "email": "contato@ong-exemplo.org",
                "senha": "",
            },
            criar=True,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("senha", form.errors)

    def test_endereco_parcial_e_rejeitado(self):
        form = OngForm(
            data={
                "cnpj": "11.222.333/0001-81",
                "razao_social": "ONG Exemplo",
                "email": "contato@ong-exemplo.org",
                "senha": "",
                "rua": "Rua das Flores",
                "numero": "10",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("bairro", form.errors)


class OngDatabaseConfigurationTests(SimpleTestCase):
    @patch("core.implementation.services.dao.connections")
    def test_alias_orm_herda_opcoes_padrao_do_django(self, conexoes):
        conexoes.databases = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
                "CONN_HEALTH_CHECKS": False,
                "ATOMIC_REQUESTS": False,
            }
        }
        connection = ConexaoBD_ORM().obter_conexao()

        alias_config = conexoes.databases[ConexaoBD_ORM.DB_ALIAS]
        self.assertIn("CONN_HEALTH_CHECKS", alias_config)
        self.assertFalse(alias_config["ATOMIC_REQUESTS"])
        self.assertIs(connection, conexoes[ConexaoBD_ORM.DB_ALIAS])


@override_settings(
    MESSAGE_STORAGE="django.contrib.messages.storage.cookie.CookieStorage"
)
class OngViewsTests(SimpleTestCase):
    def test_home_exibe_pagina_inicial(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_formulario_de_cadastro_abre(self):
        response = self.client.get(reverse("ongs_criar"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ongs/formulario.html")

    @patch("app.views._repository")
    def test_listagem_exibe_ongs_do_repositorio(self, obter_repositorio):
        ong = SimpleNamespace(
            id=7,
            razao_social="ONG Exemplo",
            cnpj="11222333000181",
            email="contato@ong-exemplo.org",
            cidade="Fortaleza",
            estado=None,
        )
        obter_repositorio.return_value.listar.return_value = [ong]

        response = self.client.get(reverse("ongs_listar"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ongs/listar.html")
        self.assertContains(response, "ONG Exemplo")
        obter_repositorio.return_value.listar.assert_called_once_with()

    @patch("app.views._repository")
    def test_cadastro_chama_repositorio_e_redireciona(self, obter_repositorio):
        response = self.client.post(
            reverse("ongs_criar"),
            {
                "cnpj": "11.222.333/0001-81",
                "razao_social": "ONG Exemplo",
                "email": "contato@ong-exemplo.org",
                "senha": "Violeta#42Abc",
            },
        )

        self.assertRedirects(response, reverse("ongs_listar"))
        obter_repositorio.return_value.criar.assert_called_once()
        ong_criada = obter_repositorio.return_value.criar.call_args.args[0]
        self.assertEqual(ong_criada.razao_social, "ONG Exemplo")
        self.assertEqual(ong_criada.email, "contato@ong-exemplo.org")

    @patch("app.views._repository")
    def test_edicao_preserva_senha_quando_nao_informada(self, obter_repositorio):
        ong = SimpleNamespace(
            id=7,
            cnpj="11222333000181",
            razao_social="ONG Exemplo",
            descricao="Descrição antiga",
            pix_para_doacao="pix@ong.org",
            email="contato@ong-exemplo.org",
            cep="",
            rua="",
            numero="",
            bairro="",
            cidade="",
            estado=EstadoBrasileiroEnum.CE,
            telefone="",
            url_foto_perfil="imgs/perfil/ong.png",
        )
        repositorio = obter_repositorio.return_value
        repositorio.buscar_id.return_value = ong
        repositorio.alterar.return_value = ong

        response = self.client.post(
            reverse("ongs_editar", kwargs={"ong_id": 7}),
            {
                "cnpj": "11.222.333/0001-81",
                "razao_social": "ONG Exemplo Atualizada",
                "descricao": "",
                "pix_para_doacao": "",
                "email": "contato@ong-exemplo.org",
                "senha": "",
                "cep": "",
                "rua": "",
                "numero": "",
                "bairro": "",
                "cidade": "",
                "estado": "",
                "telefone": "",
            },
        )

        self.assertRedirects(
            response, reverse("ongs_detalhe", kwargs={"ong_id": 7})
        )
        atualizada = repositorio.alterar.call_args.args[1]
        self.assertEqual(atualizada.senha, "")
        self.assertEqual(atualizada.url_foto_perfil, "imgs/perfil/ong.png")

    @patch("app.views._repository")
    def test_exclusao_chama_repositorio_e_redireciona(self, obter_repositorio):
        repositorio = obter_repositorio.return_value
        repositorio.buscar_id.return_value = SimpleNamespace(id=7)
        repositorio.deletar.return_value = True

        response = self.client.post(
            reverse("ongs_excluir", kwargs={"ong_id": 7})
        )

        self.assertRedirects(response, reverse("ongs_listar"))
        repositorio.deletar.assert_called_once_with(7)
