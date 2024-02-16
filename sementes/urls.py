from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.classificaSementeInicial, name='classificaSementeInicial'),
    path('classificacao/<int:id>/', views.classificacao, name='classificaSemente'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
