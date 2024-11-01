from django import forms
from .models import Employer,JobPost

class EmployerForm(forms.ModelForm):
    class Meta:
        model=Employer
        fields='__all__'

class JobpostForm(forms.ModelForm):
    class Meta:
        model=JobPost
       
        exclude=['employer']