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
    path('', views.home, name='home'),
    path('pets/', views.listar_pets, name='listar_pets'),
    path('pets/adicionar/', views.adicionar_pet, name='adicionar_pet'),
    path('pets/<int:id>/alterar/', views.alterar_pet, name='alterar_pet'),
    path('pets/<int:id>/remover/', views.remover_pet, name='remover_pet'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
