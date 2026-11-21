from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import DailyLogForm
from .models import DailyLog
from planning.models import Plan

@login_required
def mi_agenda(request):
    # 1. Verificamos que sea un docente (profesor o jefe)
    if not hasattr(request.user, 'teacherprofile'):
        raise PermissionDenied("Solo los docentes pueden acceder a la agenda.")
    
    perfil = request.user.teacherprofile
    
    # 2. Buscamos los planes APROBADOS del docente logueado
    planes_aprobados = Plan.objects.filter(teacher=perfil, status='approved')
    
    # 3. Buscamos todos los registros diarios (logs) del docente
    # Usamos el doble guion bajo para entrar desde el log -> actividad -> plan -> teacher
    logs = DailyLog.objects.filter(activity__plan__teacher=perfil).order_by('-date')
    
    return render(request, 'agenda/mi_agenda.html', {
        'planes_aprobados': planes_aprobados,
        'logs': logs
    })

@login_required
def crear_registro(request):
    if not hasattr(request.user, 'teacherprofile'):
        raise PermissionDenied("Solo los docentes pueden registrar tareas.")
    
    perfil = request.user.teacherprofile
    
    if request.method == 'POST':
        form = DailyLogForm(request.POST, request.FILES, user=request.user) # Le pasamos el usuario para filtrar actividades
        if form.is_valid():
            registro = form.save(commit=False)
            # Aquí no hay campo 'teacher' en el modelo, pero lo validamos por seguridad
            # (El formulario ya validó que la actividad sea de sus planes aprobados)
            registro.save()
            return redirect('mi_agenda')
    else:
        form = DailyLogForm(user=request.user)

    return render(request, 'agenda/crear_registro.html', {'form': form})