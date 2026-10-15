from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.implementation.services.models import Adotante, ONG, Pet, UsuarioBase


class PetInline(admin.TabularInline):
    model = Pet
    extra = 0
    fields = (
        "nome",
        "especie",
        "sexo",
        "alocacao",
        "porte",
        "moradia_recomendada",
        "disponivel",
    )


@admin.register(UsuarioBase)
class UsuarioBaseAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "tipo_usuario",
        "cidade",
        "estado",
        "is_staff",
        "is_active",
    )
    list_filter = ("tipo_usuario", "estado", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "telefone")
    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Dados do perfil",
            {
                "fields": (
                    "tipo_usuario",
                    "foto_perfil",
                    "telefone",
                    "cep",
                    "rua",
                    "numero",
                    "bairro",
                    "cidade",
                    "estado",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Dados do perfil",
            {
                "fields": (
                    "email",
                    "tipo_usuario",
                    "telefone",
                    "cep",
                    "rua",
                    "numero",
                    "bairro",
                    "cidade",
                    "estado",
                )
            },
        ),
    )


@admin.register(ONG)
class ONGAdmin(admin.ModelAdmin):
    list_display = ("razao_social", "cnpj", "pix_doacao", "total_pets")
    search_fields = ("razao_social", "cnpj", "ong__username", "ong__email")
    ordering = ("razao_social",)
    inlines = (PetInline,)

    @admin.display(description="Pets cadastrados")
    def total_pets(self, obj):
        return obj.pets_mantidos.count()


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "ong",
        "especie",
        "sexo",
        "porte",
        "alocacao",
        "disponivel",
    )
    list_filter = ("especie", "sexo", "porte", "alocacao", "disponivel", "ong")
    search_fields = ("nome", "biografia", "ong__razao_social")
    list_select_related = ("ong",)
    ordering = ("nome",)


@admin.register(Adotante)
class AdotanteAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "data_nascimento", "usuario")
    search_fields = ("nome", "cpf", "adotante__username", "adotante__email")
    ordering = ("nome",)

    @admin.display(description="Usuário")
    def usuario(self, obj):
        return obj.adotante
