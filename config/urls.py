from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# 1. Importamos la vista home de config
from . import views 

# 2. Importamos la redirección directamente desde la app users
from users.views import redireccion_login

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ruta de inicio
    path('', views.home, name='home'),
    
    # Rutas de Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Ruta de redirección (usando la importación directa)
    path('redireccion-login/', redireccion_login, name='redireccion_login'),
    
    # Apps
    path('planes/', include('planning.urls')),
    path('usuarios/', include('users.urls')),

    path('agenda/', include('agenda.urls')),
]