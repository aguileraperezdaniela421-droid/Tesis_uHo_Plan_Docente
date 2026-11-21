from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from core.mixins import jefe_required, profesor_required, docente_required
from .models import Plan, Activity
from .forms import PlanForm, ActivityForm

# --- VISTAS DEL PROFESOR ---

@docente_required
def lista_planes(request):
    # Si es profesor, solo ve sus planes
    if hasattr(request.user, 'teacherprofile') and request.user.teacherprofile.role == 'teacher':
        planes = Plan.objects.filter(teacher=request.user.teacherprofile)
    else:
        # Si es superadmin, ve todos
        planes = Plan.objects.all()
    return render(request, 'planning/lista_planes.html', {'planes': planes})

@docente_required
def crear_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            # SEGURIDAD: Forzamos al profesor logueado, ignorando el HTML
            plan.teacher = request.user.teacherprofile 
            plan.save()
            return redirect('lista_planes')
    else:
        form = PlanForm()
        # Filtramos el dropdown del form para que solo se pueda elegir a sí mismo
        form.fields['teacher'].queryset = form.fields['teacher'].queryset.filter(id=request.user.teacherprofile.id)
        form.fields['teacher'].initial = request.user.teacherprofile

    return render(request, 'planning/crear_plan.html', {'form': form})

@docente_required
def detalle_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    
    # SEGURIDAD: Un profesor no puede ver el plan de otro
    if not request.user.is_superuser and plan.teacher != request.user.teacherprofile:
        raise PermissionDenied("No tienes permiso para ver este plan.")
        
    actividades = plan.activity_set.all() 
    return render(request, 'planning/detalle_plan.html', {'plan': plan, 'actividades': actividades})

@docente_required
def crear_actividad(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id) 
    
    # SEGURIDAD: Solo el dueño del plan puede agregarle actividades
    if not request.user.is_superuser and plan.teacher != request.user.teacherprofile:
        raise PermissionDenied("No puedes agregar actividades a un plan ajeno.")
        
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            actividad = form.save(commit=False) 
            actividad.plan = plan 
            actividad.save() 
            return redirect('detalle_plan', plan_id=plan.id) 
    else:
        form = ActivityForm()

    return render(request, 'planning/crear_actividad.html', {'form': form, 'plan': plan})


# --- VISTAS DEL JEFE ---

@jefe_required
def bandeja_jefe(request):
    # Filtramos los planes pendientes SOLO del departamento del jefe
    departamento_del_jefe = request.user.teacherprofile.department
    planes_pendientes = Plan.objects.filter(
        status='pending', 
        teacher__department=departamento_del_jefe
    )
    return render(request, 'planning/bandeja_jefe.html', {'planes': planes_pendientes})

@jefe_required
def aprobar_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    
    # SEGURIDAD EXTRA: Evitar que un jefe apruebe un plan de otro departamento
    if not request.user.is_superuser and plan.teacher.department != request.user.teacherprofile.department:
        raise PermissionDenied("No puedes aprobar planes de otro departamento.")
        
    plan.status = 'approved'
    plan.save()
    return redirect('detalle_plan', plan_id=plan.id)


