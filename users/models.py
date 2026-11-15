from django.db import models
from django.contrib.auth.models import User
from institutional.models import Department

class TeacherProfile(models.Model):
    # 1. Definimos las opciones EN MAYÚSCULAS
    ROLE_CHOICES = (
        ('teacher', 'Profesor'),
        ('head', 'Jefe de Departamento'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    # 2. Aquí usamos el MISMO nombre EN MAYÚSCULAS
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='teacher')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"



