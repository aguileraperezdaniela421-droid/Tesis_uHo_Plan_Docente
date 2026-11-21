from django.urls import path
from . import views

urlpatterns = [
    path('', views.mi_agenda, name='mi_agenda'),
    path('crear/', views.crear_registro, name='crear_registro'),
]