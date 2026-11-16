from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Plan, Activity
from .forms import PlanForm, ActivityForm
from django.contrib.auth.decorators import login_required

@login_required
def lista_planes(request):
    # 1. Revisamos si el usuario tiene un perfil docente
    if hasattr(request.user, 'teacherprofile'):
        perfil = request.user.teacherprofile
        
        # 2. Si es profesor, solo ve SUS planes
        if perfil.role == 'teacher':
            planes = Plan.objects.filter(teacher=perfil)
            return render(request, 'planning/lista_planes.html', {'planes': planes})
            
        # 3. Si es jefe, ve los planes de su departamento
        elif perfil.role == 'head':
            planes = Plan.objects.filter(teacher__department=perfil.department)
            return render(request, 'planning/lista_planes.html', {'planes': planes})
            
    # 4. Si es superadmin, ve todo
    planes = Plan.objects.all()
    return render(request, 'planning/lista_planes.html', {'planes': planes})

def crear_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_planes')
    else:
        form = PlanForm()

    return render(request, 'planning/crear_plan.html', {'form': form})

def detalle_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    actividades = plan.activity_set.all() 
    return render(request, 'planning/detalle_plan.html', {'plan': plan, 'actividades': actividades})

def crear_actividad(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id) 
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

def aprobar_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    plan.status = 'approved'
    plan.save()
    return redirect('detalle_plan', plan_id=plan.id)

@login_required
def bandeja_jefe(request):
    # 1. Verificamos que realmente sea un jefe
    if not hasattr(request.user, 'teacherprofile') or request.user.teacherprofile.role != 'head':
        return redirect('home') # Si no es jefe, lo botamos al inicio

    # 2. Buscamos los planes pendientes, PERO SOLO de su departamento
    departamento_del_jefe = request.user.teacherprofile.department
    
    planes_pendientes = Plan.objects.filter(
        status='pending', # Que estén pendientes
        teacher__department=departamento_del_jefe # Y que el profesor sea de su mismo departamento
    )
    
    return render(request, 'planning/bandeja_jefe.html', {'planes': planes_pendientes})



