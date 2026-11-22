from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from core.mixins import jefe_required, profesor_required, docente_required
from .models import Plan, Activity
from .forms import PlanForm, ActivityForm

# ==========================================
# VISTAS DE PLANES (Profesores y Jefes)
# ==========================================

@docente_required
def mi_plan(request):
    perfil = request.user.teacherprofile
    mi_plan_actual = Plan.objects.filter(teacher=perfil).first()
    return render(request, 'planning/mi_plan.html', {'plan': mi_plan_actual})

@docente_required
def crear_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.teacher = request.user.teacherprofile 
            plan.save()
            return redirect('mi_plan')
    else:
        form = PlanForm()
        # Filtramos para que solo se pueda asignar el plan a sí mismo
        form.fields['teacher'].queryset = form.fields['teacher'].queryset.filter(id=request.user.teacherprofile.id)
        form.fields['teacher'].initial = request.user.teacherprofile
    return render(request, 'planning/crear_plan.html', {'form': form})

@docente_required
def detalle_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    
    if not request.user.is_superuser:
        perfil = request.user.teacherprofile
        es_el_dueno = (plan.teacher == perfil)
        es_su_jefe = (perfil.role == 'head' and plan.teacher.department == perfil.department)
        
        if not (es_el_dueno or es_su_jefe):
            raise PermissionDenied("No tienes permiso para ver este plan.")
            
    actividades = plan.activity_set.all() 
    return render(request, 'planning/detalle_plan.html', {'plan': plan, 'actividades': actividades})

@docente_required
def crear_actividad(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id) 
    
    if not request.user.is_superuser and plan.teacher != request.user.teacherprofile:
        raise PermissionDenied("No puedes agregar actividades a un plan ajeno.")
    
    if plan.status in ['pending', 'approved']:
        raise PermissionDenied("No puedes editar un plan que ya ha sido enviado o aprobado.")

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

@docente_required
def enviar_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    if not request.user.is_superuser and plan.teacher != request.user.teacherprofile:
        raise PermissionDenied("No puedes enviar un plan ajeno.")
    
    if plan.status == 'draft':
        plan.status = 'pending'
        plan.save()
    return redirect('detalle_plan', plan_id=plan.id)

# ==========================================
# VISTAS EXCLUSIVAS DEL JEFE
# ==========================================

@jefe_required
def planes_departamento(request):
    perfil = request.user.teacherprofile
    # Filtramos por su departamento y excluimos su propio plan
    planes = Plan.objects.filter(
        teacher__department=perfil.department
    ).exclude(teacher=perfil).order_by('teacher__user__username')
    
    return render(request, 'planning/planes_departamento.html', {'planes': planes})

@jefe_required
def bandeja_jefe(request):
    perfil = request.user.teacherprofile
    planes_pendientes = Plan.objects.filter(
        status='pending',
        teacher__department=perfil.department
    ).exclude(teacher=perfil)
    
    return render(request, 'planning/bandeja_jefe.html', {'planes': planes_pendientes})

@jefe_required
def aprobar_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    
    if not request.user.is_superuser and plan.teacher.department != request.user.teacherprofile.department:
        raise PermissionDenied("No puedes aprobar planes de otro departamento.")
        
    if not request.user.is_superuser and plan.teacher == request.user.teacherprofile:
        raise PermissionDenied("No puedes aprobar tu propio plan.")

    plan.status = 'approved'
    plan.save()
    return redirect('detalle_plan', plan_id=plan.id)
