from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_planes, name='lista_planes'),
    path('crear/', views.crear_plan, name='crear_plan'),
    path('bandeja/', views.bandeja_jefe, name='bandeja_jefe'),
    path('<int:plan_id>/', views.detalle_plan, name='detalle_plan'),
    path('<int:plan_id>/crear-actividad/', views.crear_actividad, name='crear_actividad'),
    path('<int:plan_id>/aprobar/', views.aprobar_plan, name='aprobar_plan'),
]