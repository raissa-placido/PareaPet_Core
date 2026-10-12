from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from app import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.usuario_urls", namespace="usuario_pp")),
    path("", views.home, name="home"),
    path("ongs/", views.listar_ongs, name="ongs_listar"),
    path("ongs/nova/", views.criar_ong, name="ongs_criar"),
    path("ongs/<int:ong_id>/", views.detalhe_ong, name="ongs_detalhe"),
    path("ongs/<int:ong_id>/editar/", views.editar_ong, name="ongs_editar"),
    path("ongs/<int:ong_id>/excluir/", views.excluir_ong, name="ongs_excluir"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
