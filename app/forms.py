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