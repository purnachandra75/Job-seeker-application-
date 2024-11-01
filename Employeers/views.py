from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import EmployerForm,JobpostForm
from .models import Employer,JobPost
from django.views.generic.edit import FormView,CreateView
from django.views.generic.base import TemplateView
from django.views.generic import ListView

from job_seekers.models import Personalinfo,Education,WorkExperience,Languages,Skill,Applicant


def registerEmp(request):
    if request.method =="GET":
        return render(request,'registeremp.html',{'e_form':EmployerForm()})
    if request.method =='POST':
        somedata=EmployerForm(request.POST)
        if somedata.is_valid():
            somedata.save()
            return render(request,'homepage.html')
        return render(request,'registeremp.html',{'e_form':EmployerForm(),'msg':'pelase insert valid data'})

class Homepage(TemplateView):
    template_name='homepage.html' 
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)   
        return context 
class CreateEmp(FormView):
    form_class=EmployerForm
    template_name='createempprofile.html'
    success_url='homepage.html'
    def form_valid(self, Form):
        Form.save()
        return super.form_valid(Form)

class Createjob(CreateView):
    template_name='createjobpost.html'
    model=JobPost
    fields='__all__'
    exclude=['employer']
    success_url= reverse_lazy('homepage')
class Viewpostedjobs(TemplateView):

    template_name='listofjobs.html'
    def get_context_data(self, **kwargs): 
        context=super().get_context_data(**kwargs)
        user=kwargs['user']
        somedata=Employer.objects.get(full_name=user)
        context['listofjobs']=JobPost.objects.filter(employer_id=somedata.id)
        return context

class Moredetails(TemplateView):
    template_name='moredetails.html'
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        uid=kwargs['id']
        context['personalinfo']=Personalinfo.objects.get(id=uid)
        context['eduinfo']=Education.objects.filter(User_id=uid)
        context['skills']=Skill.objects.filter(User_id=uid)
        context['lang']=Languages.objects.filter(User_id=uid)
        context['workexp']=WorkExperience.objects.filter(User_id=uid)
        return context

class Moreabout(TemplateView):
    template_name = 'moredetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hint = kwargs['skill']

        
        somedata = Skill.objects.filter(Skillname=hint)
        info=[]
        for eachone in somedata:
            uid = eachone.User_id
            d={}
            
            d['personal_info']= Personalinfo.objects.filter(id=uid)
            d['education_info'] = Education.objects.filter(User_id=uid)
            d['skills_info'] = Skill.objects.filter(User_id=uid)
            d['languages_info'] = Languages.objects.filter(User_id=uid)
            d['workexp_info'] = WorkExperience.objects.filter(User_id=uid)
            
            info.append(d)
        context['data']=info
        return context

class ListofApplicants(TemplateView):
    template_name='listofApplicants.html'
    def get_context_data(self, **kwargs): 
        contaxt= super().get_context_data(**kwargs)
        jobid=kwargs['jobid']
        somedata=Applicant.objects.filter(Job_id=jobid)
        l=[]
        for eachdata in somedata:
            l.append(Personalinfo.objects.filter(id=eachdata.seeker_id))
        contaxt['apllicants']=l
        return contaxt

class AboutJobseeker(TemplateView):
    template_name='aboutjobseeker.html'
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        uid=kwargs['id']
        context['personalinfo']=Personalinfo.objects.get(id=uid)
        context['eduinfo']=Education.objects.filter(User_id=uid)
        context['skills']=Skill.objects.filter(User_id=uid)
        context['lang']=Languages.objects.filter(User_id=uid)
        context['workexp']=WorkExperience.objects.filter(User_id=uid)
        return context
        
class ListofJobSekers(ListView):
    template_name='listofjobseekers.html'
    model=Personalinfo
    def get_queryset(self) :
        alldata=super().get_queryset()
        res=alldata.filter(profile_status='active')
        return res
# Create your views here.
