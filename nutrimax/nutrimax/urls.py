"""
URL configuration for nutrimax project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from app_nutrimax import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.home, name='home'),
    path('pages/listagem_usuarios/', views.usuarios, name= 'listagem_usuarios'),
    path('pages/base_usuarios/', views.base_usuarios, name= 'base_usuarios'),
    path('pages/recomendacao_nutricional/', views.recomendacao_nutricional, name= 'recomendacao_nutricional'),
    path('pages/recomendacao_nutricional/<int:usuario_id>/', views.recomendacao_nutricional, name='recomendacao_nutricional_com_usuario'),
    path('pages/alimentos/', views.alimentos, name= 'alimentos'),
    path('pages/cadastra_alimentos/', views.cadastra_alimentos, name= 'cadastra_alimentos'),
    path('criador_cardapio/', views.criador_cardapio, name='criador_cardapio'),
    path('salvar_cardapio/', views.salvar_cardapio, name='salvar_cardapio'),
    path('visualizar_cardapio/<int:usuario_id>/', views.visualizar_cardapio, name='visualizar_cardapio')
]
