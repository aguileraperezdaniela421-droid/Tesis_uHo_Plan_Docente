from django.shortcuts import render, redirect, get_object_or_404
from .models import Plan
from .forms import PlanForm

def lista_planes(request):
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