from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from app import views

urlpatterns = [

    ### django admin e home
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),

    ### urls para adotante
    path("", include("app.usuario_urls", namespace="usuario_pp")),

    # urls para ong
    path("ongs/", views.listar_ongs, name="ongs_listar"),
    path("ongs/nova/", views.criar_ong, name="ongs_criar"),
    path("ongs/<int:ong_id>/", views.detalhe_ong, name="ongs_detalhe"),
    path("ongs/<int:ong_id>/editar/", views.editar_ong, name="ongs_editar"),
    path("ongs/<int:ong_id>/excluir/", views.excluir_ong, name="ongs_excluir"),

    ### urls para pet
    path('pets/', views.listar_pets, name='listar_pets'),
    path('pets/adicionar/', views.adicionar_pet, name='adicionar_pet'),
    path('pets/<int:id>/alterar/', views.alterar_pet, name='alterar_pet'),
    path('pets/<int:id>/remover/', views.remover_pet, name='remover_pet'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
