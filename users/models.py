from django.db import models
from django.contrib.auth.models import User
from institutional.models import Department

class TeacherProfile(models.Model):
    ROLE_CHOICES = (
        ('teacher', 'Profesor'),
        ('head', 'Jefe de Departamento'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aga_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    ci = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='teacher')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    phone = models.CharField(max_length=20, blank=True, null=True)
    academic_category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"



