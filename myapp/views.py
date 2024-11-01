from django.shortcuts import render
from Employeers.models import JobPost
# Create your views here.
def get_homepage(request):
    jobs=JobPost.objects.all()
    return render(request,'welcomepage.html',{'jobs':jobs})
def get_home(request):
    jobs=JobPost.objects.all()
    return render(request,'welcomepage.html',{'jobs':jobs})
def get_about(request):
    return render(request,'about.html')
def get_contact(request):
    return render(request,'contact.html')
