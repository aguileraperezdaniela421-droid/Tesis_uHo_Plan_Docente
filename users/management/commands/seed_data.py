from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from institutional.models import Campus, Faculty, Department, Dimension
from users.models import TeacherProfile
from planning.models import Period, Plan, Activity
from datetime import date

class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write("Borrando datos viejos...")
        # (Opcional) Descomenta si quieres que borre todo antes de insertar
        # User.objects.exclude(is_superuser=True).delete()
        # Campus.objects.all().delete()
        
        self.stdout.write("Creando estructura institucional...")
        campus = Campus.objects.create(name="Campus Central", code="HOL-01")
        facultad = Faculty.objects.create(name="Facultad de Ingeniería", code="ING", campus=campus)
        depto_info = Department.objects.create(name="Departamento de Informática", code="INFO", faculty=facultad)
        depto_med = Department.objects.create(name="Departamento de Medicina", code="MED", faculty=facultad)
        
        self.stdout.write("Creando dimensiones...")
        dim_docencia = Dimension.objects.create(name="Docencia")
        dim_investigacion = Dimension.objects.create(name="Investigación")

        self.stdout.write("Creando usuarios y perfiles...")
        # 1. Jefe de Informática
        jefe_user = User.objects.create_user(username='jefe_info', password='123456', email='jefe@uho.edu.cu')
        jefe_perfil = TeacherProfile.objects.create(user=jefe_user, department=depto_info, role='head', status='active')

        # 2. Profesor de Informática
        prof_user = User.objects.create_user(username='prof_info', password='123456', email='prof@uho.edu.cu')
        prof_perfil = TeacherProfile.objects.create(user=prof_user, department=depto_info, role='teacher', status='active')

        # 3. Profesor de Medicina (Para probar que el jefe de info no lo vea)
        prof_med_user = User.objects.create_user(username='prof_med', password='123456')
        prof_med_perfil = TeacherProfile.objects.create(user=prof_med_user, department=depto_med, role='teacher', status='active')

        self.stdout.write("Creando períodos y planes...")
        periodo = Period.objects.create(name="Curso 2026-2027", start_date=date(2026,9,1), end_date=date(2027,7,15))
        
        # Plan para el profesor de informática
        plan_info = Plan.objects.create(teacher=prof_perfil, period=periodo, status='pending')
        Activity.objects.create(plan=plan_info, dimension=dim_docencia, name="Clases de Programación", planned_hours=120)
        Activity.objects.create(plan=plan_info, dimension=dim_investigacion, name="Proyecto de IA", planned_hours=80)

        # Plan para el profesor de medicina
        plan_med = Plan.objects.create(teacher=prof_med_perfil, period=periodo, status='draft')

        self.stdout.write(self.style.SUCCESS("¡Base de datos poblada con éxito!"))
        self.stdout.write("Usuarios creados: jefe_info / prof_info / prof_med (password: 123456)")