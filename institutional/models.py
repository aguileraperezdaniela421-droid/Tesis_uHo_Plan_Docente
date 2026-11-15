from django.db import models

class Campus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.campus.name})"
