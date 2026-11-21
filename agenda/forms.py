from django import forms
from .models import DailyLog
from planning.models import Activity

class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = ['activity', 'date', 'description', 'executed_hours', 'result', 'evidence', 'is_extraordinary', 'justification']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'result': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'justification': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'activity': forms.Select(attrs={'class': 'form-select'}),
            'executed_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'evidence': forms.FileInput(attrs={'class': 'form-control'}),
            'is_extraordinary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # Sacamos el usuario
        super().__init__(*args, **kwargs)
        
        if user and hasattr(user, 'teacherprofile'):
            # Filtramos para que solo vea sus actividades aprobadas
            self.fields['activity'].queryset = Activity.objects.filter(
                plan__teacher=user.teacherprofile, 
                plan__status='approved'
            )
        else:
            self.fields['activity'].queryset = Activity.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        activity = cleaned_data.get('activity')
        is_extraordinary = cleaned_data.get('is_extraordinary')
        justification = cleaned_data.get('justification')

        if is_extraordinary and not justification:
            self.add_error('justification', 'Debes justificar por qué esta tarea es extraordinaria.')
        
        if not is_extraordinary and not activity:
            self.add_error('activity', 'Si no es extraordinaria, debes seleccionar una actividad de tu plan.')

        return cleaned_data