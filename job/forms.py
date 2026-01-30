from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['company_name', 'role', 'applied_date', 'status', 'notes']
        widgets = {
            'applied_date': forms.DateInput(attrs={'type': 'date'}),
        }
