from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TeacherProfile
from institutional.models import Department

# 1. FORMULARIO DE REGISTRO
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingresa un correo válido.")
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), 
        label="Departamento al que perteneces",
        empty_label="Selecciona tu departamento..."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # SEGURIDAD: Forzamos el rol a 'teacher' sin importar lo que venga del HTML
            TeacherProfile.objects.create(
                user=user,
                department=self.cleaned_data['department'],
                role='teacher', 
                status='active' # O 'pending' si quieres que un admin lo apruebe primero
            )
        return user

# 2. FORMULARIO PARA EDITAR EL PERFIL
class PerfilForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['phone', 'academic_category', 'ci', 'aga_id']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_category': forms.TextInput(attrs={'class': 'form-control'}),
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'aga_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'phone': 'Teléfono',
            'academic_category': 'Categoría Docente',
            'ci': 'Carnet de Identidad',
            'aga_id': 'ID AGA',
        }