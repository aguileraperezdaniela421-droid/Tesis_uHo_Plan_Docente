from django import forms
from .models import Plan, Activity

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['teacher', 'period']

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'dimension', 'description', 'planned_hours']
        