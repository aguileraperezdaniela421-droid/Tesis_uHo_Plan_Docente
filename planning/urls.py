from django.urls import path
from . import views

urlpatterns = [
    path('mi-plan/', views.mi_plan, name='mi_plan'),
    path('mi-plan/crear/', views.crear_plan, name='crear_plan'),
    path('departamento/', views.planes_departamento, name='planes_departamento'),
    path('bandeja/', views.bandeja_jefe, name='bandeja_jefe'),
    path('<int:plan_id>/', views.detalle_plan, name='detalle_plan'),
    path('<int:plan_id>/crear-actividad/', views.crear_actividad, name='crear_actividad'),
    path('<int:plan_id>/enviar/', views.enviar_plan, name='enviar_plan'),
    path('<int:plan_id>/aprobar/', views.aprobar_plan, name='aprobar_plan'),
]