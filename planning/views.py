from django.shortcuts import render, redirect
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