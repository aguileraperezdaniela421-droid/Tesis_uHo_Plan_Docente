from django.db import models
from planning.models import Activity

class DailyLog(models.Model):
    # Relación (Opcional para permitir tareas extraordinarias)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='logs', null=True, blank=True)
    
    # Datos de la tarea
    date = models.DateField(help_text="Fecha en que se ejecutó la tarea")
    description = models.TextField(help_text="Describe qué hiciste exactamente")
    executed_hours = models.DecimalField(max_digits=5, decimal_places=2, help_text="Horas dedicadas")
    result = models.TextField(blank=True, null=True, help_text="Resultado obtenido de la tarea")
    
    # Evidencia
    evidence = models.FileField(upload_to='evidencias/', null=True, blank=True, help_text="Sube un PDF o imagen de prueba")
    
    # Tareas Extraordinarias (RF-21 / Sección 5)
    is_extraordinary = models.BooleanField(default=False, help_text="Marca si es una tarea no planificada")
    justification = models.TextField(blank=True, null=True, help_text="Explica por qué esta tarea es extraordinaria")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.activity:
            return f"{self.date} - {self.activity.name} ({self.executed_hours}h)"
        return f"{self.date} - Tarea Extraordinaria ({self.executed_hours}h)"
