from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.mi_perfil, name='mi_perfil'),
]