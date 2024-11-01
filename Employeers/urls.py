from django.urls import path
from . import views
 

urlpatterns=[
    path('registeremp/',views.registerEmp,name='registeremp'),
    path('homepage/',views.Homepage.as_view(),name='homepage'),
    path('createempprofile/',views.CreateEmp.as_view(),name='createempprofile'),
    path('createjobpost/',views.Createjob.as_view(),name='createjobpost'),
    path('listofjob/<str:user>',views.Viewpostedjobs.as_view(),name='listofjobs'),
    path('searchingforjobseeker/',views.ListofJobSekers.as_view(),name='searchingforjobseeker'),
    path('moredetails/<int:id>',views.Moredetails.as_view(),name='moredetails'),
    path('searchingforjobseeker/<str:skill>',views.Moreabout.as_view(),name='searchingforjobseeker'),
    path('listofapplicants/<int:jobid>',views.ListofApplicants.as_view(),name='listofapplicants'),
    path('aboutjobseeker/<int:id>',views.AboutJobseeker.as_view(),name='aboutjobseeker')
]