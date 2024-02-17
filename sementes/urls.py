from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.classificaSementeInicial, name='classificaSementeInicial'),
    path('classificacao/<int:id>/', views.classificacao, name='classificaSemente'),
    path('classificar/', views.classifica, name='classificar'),
    path('criar_em_massa/', views.criar_sementes_em_massa, name='criarSementesEmMassa'),

]