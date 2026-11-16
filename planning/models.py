from django.db import models
from users.models import TeacherProfile
from institutional.models import Dimension

class Period(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Plan(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Borrador'),
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    )
    
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    observation = models.TextField(blank=True, null=True)
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('teacher', 'period')

    def __str__(self):
        return f"Plan de {self.teacher.user.username} - {self.period.name}"

class Activity(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    dimension = models.ForeignKey(Dimension, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    expected_results = models.TextField(blank=True, null=True)
    indicator = models.CharField(max_length=255, blank=True, null=True)
    target = models.IntegerField(null=True, blank=True)
    planned_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} ({self.planned_hours}h)"





