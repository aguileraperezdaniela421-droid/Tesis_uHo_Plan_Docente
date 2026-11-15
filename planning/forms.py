from .models import Plan, Activity # Asegúrate de importar Activity también
from django import forms

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['teacher', 'period']


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'planned_hours']
        