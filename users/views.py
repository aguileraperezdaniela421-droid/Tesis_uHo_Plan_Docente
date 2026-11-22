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

from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import redirect

def redireccion_login(request):
    # Después de loguearse, todos van a la página de inicio (Home)
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