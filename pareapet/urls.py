"""
URL configuration for proj_bd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # define as rotas de URL da nossa aplicacao
    path('', views.home, name='home'),
    
    # path('instrucoes/', 'instrucoes/instrucoes.html', name='instrucoes'),



    # ===========================================================================
    # Rotas: CATEGORIA
    #   - categorias/              : exibe página de listagem
    #   - categorias/incluir/      : exibe a página de inclusao de registro
    #   - categorias/alterar/<id>/ : exibe a página de alteracao de registro
    #   - categorias/excluir/<id>/ : exibe a página de exclusao de registro
    #   - categorias/salvar/       : insere, altera ou exclui um registro do BD
    # 
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/<str:acao>/', views.categorias, name='categorias' ), 
    path('categorias/<str:acao>/<int:id>/', views.categorias, name='categorias'),

    # ===========================================================================
    # Rotas: PRODUTO
    #   - produtos/              : exibe página de listagem
    #   - produtos/incluir/      : exibe a página de inclusao de registro
    #   - produtos/alterar/<id>/ : exibe a página de alteracao de registro
    #   - produtos/excluir/<id>/ : exibe a página de exclusao de registro
    #   - produtos/salvar/       : insere, altera ou exclui um registro do BD
    # 
    # 
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/<str:acao>/', views.produtos, name='produtos' ), 
    path('produtos/<str:acao>/<int:id>/', views.produtos, name='produtos'),

] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
