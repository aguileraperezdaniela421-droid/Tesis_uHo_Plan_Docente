from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroUsuarioForm, PerfilForm
from .models import TeacherProfile

def registro(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta creada exitosamente! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'users/registro.html', {'form': form})

def redireccion_login(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_superuser or request.user.is_staff:
        return redirect('/admin/')
    
    if hasattr(request.user, 'teacherprofile'):
        perfil = request.user.teacherprofile
        if perfil.role == 'head':
            return redirect('bandeja_jefe') 
        elif perfil.role == 'teacher':
            return redirect('lista_planes')
    
    return redirect('home')

@login_required
def mi_perfil(request):
    try:
        perfil = request.user.teacherprofile
    except TeacherProfile.DoesNotExist:
        return redirect('/admin/')

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tus datos han sido actualizados correctamente.')
            return redirect('mi_perfil')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'users/mi_perfil.html', {'form': form, 'perfil': perfil})