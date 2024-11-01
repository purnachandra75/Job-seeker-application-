from django.urls import path,include
from . import views

urlpatterns = [
    
    path('',views.get_homepage),
    path('home/',views.get_home,name='home'),
    path('about/',views.get_about,name='about'),
    path('contact/',views.get_contact,name='contact')

]