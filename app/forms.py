from django import forms

from app.factory import ServicosFactory
from core.domain.entities.enums import (
    AlocacaoEnum,
    EspecieEnum,
    MoradiaEnum,
    PorteEnum,
    SexoAnimalEnum,
)
from core.implementation.services.models import ONG, Pet


def _enum_choices(enum_class, empty_label):
    return [("", empty_label)] + [
        (item.codigo, item.descricao) for item in enum_class
    ]


class PetForm(forms.Form):
    ong = forms.ModelChoiceField(label="ONG", queryset=ONG.objects.none())
    especie = forms.TypedChoiceField(
        label="Espécie",
        choices=_enum_choices(EspecieEnum, "Selecione uma espécie"),
        coerce=int,
    )
    sexo = forms.TypedChoiceField(
        label="Sexo",
        choices=_enum_choices(SexoAnimalEnum, "Selecione o sexo do animal"),
        coerce=int,
    )
    nome = forms.CharField(label="Nome", max_length=100)
    data_nascimento = forms.DateField(
        label="Data de nascimento",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        input_formats=["%Y-%m-%d"],
    )
    alocacao = forms.TypedChoiceField(
        label="Alocação",
        choices=_enum_choices(AlocacaoEnum, "Selecione a alocação"),
        coerce=int,
    )
    porte = forms.TypedChoiceField(
        label="Porte",
        choices=_enum_choices(PorteEnum, "Informe o porte do animal"),
        coerce=int,
    )
    moradia_recomendada = forms.TypedChoiceField(
        label="Moradia recomendada",
        choices=_enum_choices(
            MoradiaEnum, "Informe a moradia recomendada"
        ),
        coerce=int,
    )
    disponivel = forms.BooleanField(
        label="Disponível",
        required=False,
        initial=True,
    )
    biografia = forms.CharField(
        label="Biografia",
        required=False,
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db_alias = ServicosFactory().obter_conexao_bd().DB_ALIAS
        self.fields["ong"].queryset = ONG.objects.using(db_alias).order_by(
            "razao_social"
        )


class PetModelForm(forms.ModelForm):
    """Formulário baseado no model para uso direto no admin ou extensões."""

    class Meta:
        model = Pet
        fields = "__all__"
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


class AdotanteForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    nome = forms.CharField(label="Nome", max_length=50, required=False)
    cpf = forms.CharField(label="CPF", max_length=14, required=False)
    data_nascimento = forms.DateField(
        label="Data de nascimento",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    email = forms.EmailField(label="E-mail", max_length=254, required=True)
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(render_value=False),
        required=False,
    )
    telefone = forms.CharField(label="Telefone", max_length=20, required=False)
    cep = forms.CharField(label="CEP", max_length=9, required=False)
    rua = forms.CharField(label="Rua", max_length=100, required=False)
    numero = forms.CharField(label="Número", max_length=20, required=False)
    bairro = forms.CharField(label="Bairro", max_length=50, required=False)
    cidade = forms.CharField(label="Cidade", max_length=50, required=False)
    estado = forms.ChoiceField(
        label="Estado",
        required=False,
        choices=[("", "Selecione")]
        + [(estado.codigo, estado.descricao) for estado in EstadoBrasileiroEnum],
    )

    def __init__(self, *args, is_update=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["senha"].required = not is_update
        if is_update:
            self.fields["senha"].help_text = (
                "Deixe em branco para manter a senha atual."
            )
