from django import forms
from .models import Personalinfo,Education,Skill,WorkExperience,Languages

class parsonalinfoForm(forms.ModelForm):
    class Meta:
        model=Personalinfo
        fields='__all__'


class EducationForm(forms.ModelForm):
    class Meta:
        model=Education
        
        exclude=['User']

class SkillForm(forms.ModelForm):
    class Meta:
        model=Skill
        exclude=['User']

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model=WorkExperience
        exclude=['User']

class LanguagesForm(forms.ModelForm):
    class Meta:
        model=Languages
        exclude=['User']