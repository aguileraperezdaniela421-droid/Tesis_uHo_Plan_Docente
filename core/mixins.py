from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from functools import wraps

# --- MIXINS (Para Vistas Basadas en Clases - Futuro) ---
class JefeRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if hasattr(request.user, 'teacherprofile') and request.user.teacherprofile.role == 'head':
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("No tienes permiso de Jefe para estar aquí.")

class ProfesorRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if hasattr(request.user, 'teacherprofile') and request.user.teacherprofile.role == 'teacher':
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("No tienes permiso de Profesor para estar aquí.")


# --- DECORADORES (Para tus Vistas Basadas en Funciones actuales) ---
def jefe_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if hasattr(request.user, 'teacherprofile') and request.user.teacherprofile.role == 'head':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Solo los jefes pueden acceder aquí.")
    return _wrapped_view

def profesor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if hasattr(request.user, 'teacherprofile') and request.user.teacherprofile.role == 'teacher':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Solo los profesores pueden acceder aquí.")
    return _wrapped_view

def docente_required(view_func):
    """Permite el paso a profesores y jefes (cualquier usuario con TeacherProfile)."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if hasattr(request.user, 'teacherprofile'):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Debes ser un docente registrado para acceder aquí.")
    return _wrapped_view