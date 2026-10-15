from django import forms
from django.contrib.auth.password_validation import validate_password

from core.domain.entities.enums import EstadoBrasileiroEnum


class OngForm(forms.Form):
    cnpj = forms.CharField(label="CNPJ", max_length=18)
    razao_social = forms.CharField(label="Razão social", max_length=255)
    descricao = forms.CharField(
        label="Descrição",
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
    )
    pix_para_doacao = forms.CharField(
        label="Chave PIX para doação", max_length=50, required=False
    )
    email = forms.EmailField(label="E-mail", max_length=150)
    senha = forms.CharField(
        label="Senha",
        required=False,
        widget=forms.PasswordInput(render_value=False),
    )
    cep = forms.CharField(label="CEP", max_length=9, required=False)
    rua = forms.CharField(label="Rua", max_length=100, required=False)
    numero = forms.CharField(label="Número", max_length=20, required=False)
    bairro = forms.CharField(label="Bairro", max_length=50, required=False)
    cidade = forms.CharField(label="Cidade", max_length=50, required=False)
    estado = forms.ChoiceField(
        label="Estado",
        required=False,
        choices=[("", "Selecione um estado")]
        + [(item.codigo, item.descricao) for item in EstadoBrasileiroEnum],
    )
    telefone = forms.CharField(label="Telefone", max_length=20, required=False)

    def __init__(self, *args, ong=None, criar=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["senha"].required = criar

        if ong is not None:
            self.initial.update(
                {
                    "cnpj": ong.cnpj,
                    "razao_social": ong.razao_social,
                    "descricao": ong.descricao,
                    "pix_para_doacao": ong.pix_para_doacao,
                    "email": ong.email,
                    "cep": ong.cep,
                    "rua": ong.rua,
                    "numero": ong.numero,
                    "bairro": ong.bairro,
                    "cidade": ong.cidade,
                    "estado": ong.estado.codigo if ong.estado else "",
                    "telefone": ong.telefone,
                }
            )

    def clean(self):
        dados = super().clean()
        campos_endereco = ("rua", "numero", "bairro")
        if any(dados.get(campo) for campo in campos_endereco):
            for campo in campos_endereco:
                if not dados.get(campo):
                    self.add_error(
                        campo,
                        "Preencha rua, número e bairro para informar o endereço.",
                    )
        return dados

    def clean_senha(self):
        senha = self.cleaned_data.get("senha")
        if senha:
            validate_password(senha)
        return senha
