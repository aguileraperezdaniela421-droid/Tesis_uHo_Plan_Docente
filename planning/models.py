from django.db import models
from users.models import TeacherProfile

class Period(models.Model):
    name = models.CharField(max_length=100) 
    def __str__(self):
        return self.name


class Plan(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='draft') 

    observation = models.TextField(blank=True, null=True, help_text="Observaciones del jefe de departamento")
    
    class Meta:
        unique_together = ('teacher', 'period') 

    def __str__(self):
        return f"Plan de {self.teacher.user.username} - {self.period.name}"


class Activity(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    name = models.CharField(max_length=200) # Ej: "Dar clases de Programación"
    planned_hours = models.IntegerField() 
    
    def __str__(self):
        return f"{self.name} ({self.planned_hours}h) - {self.plan}"



