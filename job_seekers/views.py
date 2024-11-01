from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from .models import Personalinfo,Education,WorkExperience,Languages,Skill,Applicant
from .forms import EducationForm,parsonalinfoForm,WorkExperienceForm,LanguagesForm,SkillForm
from django.views import View

from Employeers.models import JobPost

def createprofile(request):
    if request.method=='GET':
        pform = parsonalinfoForm()
        eform = EducationForm()
        wform = WorkExperienceForm()
        sform = SkillForm()
        lform = LanguagesForm()

        return render(request, 'createprofile.html', {
            'pform': pform,
            'eform': eform,
            'wform': wform,
            'sform': sform,
            'lform': lform,
        })
    elif request.method=='POST':
        new_data=parsonalinfoForm(request.POST)
        name = request.POST.get('Name')
        
        if new_data.is_valid():
            new_data.save()
            uid=Personalinfo.objects.get(Name=name)
            
            
            print(uid.id)
            eform=EducationForm(request.POST)
            if eform.is_valid():
                e_data=eform.save(commit=False)
                e_data.User_id=uid.id
                e_data.save()
            
            sform=SkillForm(request.POST)
            
            if sform.is_valid():
                s_data = sform.save(commit=False)
                s_data.User_id = uid.id
                s_data.save()
                print('Skill data saved:', s_data)
            else:
                print("SkillForm errors:", sform.errors)
            
            wform=WorkExperienceForm(request.POST)
            if wform.is_valid():
                w_data=wform.save(commit=False)
                w_data.User_id=uid.id
                w_data.save()
            lform=LanguagesForm(request.POST)
            if lform.is_valid():
                l_data=lform.save(commit=False)
                l_data.User_id=uid.id
                l_data.save()
            

            
                return render(request,'home.html')
        # return render(request,'createprofile.html',{'pform':parsonalinfoForm(),'eform':EducationForm})
    return HttpResponse("bad...!!!")
def viewProfile(request):
    
    p_data=Personalinfo.objects.get(Name=request.user)
    print(p_data.Name,p_data.id)
    e_data=Education.objects.filter(User_id =p_data.id)
    w_data=WorkExperience.objects.filter(User_id=p_data.id)
    l_data=Languages.objects.filter(User_id=p_data.id)
    s_data=Skill.objects.filter(User_id=p_data.id)

    
    return render(request,'viewprofile.html',{'p_data':p_data,'e_data':e_data,'w_data':w_data,'l_data':l_data,'s_data':s_data})
def delete(request,pk):
    somedata=Education.objects.get(id=pk)
    somedata.delete()
    return redirect('updateEducation',somedata.User_id) 
def add(request,uid):
    if request.method == 'GET':
        return render(request,'updateprofile.html',{'msg':'add' ,'form':EducationForm()})
    if request.method == 'POST':
        somedata=EducationForm(request.POST)
        newdata=somedata.save(commit=False)
        newdata.User_id=uid
        newdata.save()
        return redirect('updateEducation',uid)
def update(request,pk,uid):
    if request.method == "GET":

        somedata=Education.objects.get(id=pk)
        somedata.delete()
        return render(request,'updateprofile.html',{'msg':'update' ,'form':EducationForm(instance=somedata)})

    if request.method=="POST":
        somedata=EducationForm(request.POST)
        
        if somedata.is_valid():
            newdata=somedata.save(commit=False)
            newdata.User_id=uid
            newdata.save()
        return redirect('updateEducation',newdata.User_id) 
def updateEducation(request, id):
    try:
        # Retrieve existing education records for the user
        e_data = Education.objects.filter(User_id=id)
        
        
    except Education.DoesNotExist:
        raise Http404("Education record does not exist for the given User ID")

    if request.method == 'GET':
        if not e_data.exists():
            return render(request, 'updateprofile.html', {'msg': 'add', 'form': EducationForm()})

       
        # Show the form and existing data when GET request is made
        return render(request, 'updateprofile.html', {
            'e_form': EducationForm(),  # Empty form for adding new records
            'e_data': e_data  # Existing records to display
        })

    elif request.method == 'POST':
        # Handle the form submission
        e_form = EducationForm(request.POST)
        
        if e_form.is_valid():
            e_instance = e_form.save(commit=False)
            e_instance.User_id = id
            e_instance.save()
            p_data=Personalinfo.objects.get(id=id)
            # Redirect to prevent resubmission
            return redirect('Viewprofile',p_data.Name)
        else:
            # Return the form with errors
            return render(request, 'updateprofile.html', {
                'e_form': e_form,  # Form with validation errors
                'e_data': e_data,
                'msg': 'There was an error updating the information.'
            })
def updateSkill(request,uid):
    
    
    has_education = Skill.objects.filter(User_id=uid).exists()
    
    if request.method == "GET":
        if not has_education:
            return render(request, 'updatedskills.html', {'form': SkillForm()})
        else:
            s_data=Skill.objects.filter(User_id=uid)
            return render(request, 'updatedskills.html', {'form': SkillForm(), 's_data': s_data})
        
def updateNewSkill(request,pk,uid):
    if request.method=='GET':
        somedata=Skill.objects.get(id=pk)
        somedata.delete()
        return render(request,'updatedskills.html',{'msg':'update','form':SkillForm(instance=somedata)})
    if request.method == 'POST':
        somedata=SkillForm(request.POST)
        
        if somedata.is_valid():
            newdata=somedata.save(commit=False)
            newdata.User_id=uid
            newdata.save()
            
        return redirect('updateskill',uid)


def deleteskills(request,uid):
    somedata=Skill.objects.get(id=uid)
    somedata.delete()
    return redirect('updateskill',somedata.User_id) 


def updateworkexp(request,uid):
    has_education = WorkExperience.objects.filter(User_id=uid).exists()
    
    if request.method == "GET":
        if not has_education:
            return render(request, 'updateworkexp.html', {'form': WorkExperienceForm()})
        else:
            w_data=WorkExperience.objects.filter(User_id=uid)
            return render(request, 'updateworkexp.html', {'form': WorkExperienceForm(), 'w_data': w_data})
        
def addworkexp(request,user):
    sdata=Personalinfo.objects.get(Name=user)
    if request.method == 'GET':
        
        

        return render(request,'updateworkexp.html',{'msg':'add' ,'form':WorkExperienceForm()})
    if request.method == 'POST':
        somedata=WorkExperienceForm(request.POST)
        if somedata.is_valid():
            newdata=somedata.save(commit=False)
            newdata.User_id=sdata.id
            newdata.save()
            return redirect('updateWorkExp',sdata.id)

def deleteworkexp(request,pk):
    somedata=WorkExperience.objects.get(id=pk)
    somedata.delete()
    return redirect('updateWorkExp',somedata.User_id)       

def updatenewworkexp(request,pk,uid):
    if request.method=='GET':
        somedata=WorkExperience.objects.get(id=pk)
        somedata.delete()
        return render(request,'updateworkexp.html',{'msg':'update','form':WorkExperienceForm(instance=somedata)})
    if request.method == 'POST':
        somedata=WorkExperienceForm(request.POST)
        
        if somedata.is_valid():
            newdata=somedata.save(commit=False)
            newdata.User_id=uid
            newdata.save()
            
        return redirect('updateWorkExp',uid)

def updateLang(request,uid):
    has_education = Languages.objects.filter(User_id=uid).exists()
    
    if request.method == "GET":
        if not has_education:
            return render(request, 'updatelang.html', {'form': LanguagesForm()})
        else:
            l_data=Languages.objects.filter(User_id=uid)
            return render(request, 'updatelang.html', {'form':LanguagesForm(), 'l_data': l_data})

def addlang(request,user):  
    sdata=Personalinfo.objects.get(Name=user)
    if request.method == 'GET':
        
        

        return render(request,'updatelang.html',{'msg':'add' ,'form':LanguagesForm()})
    if request.method == 'POST':
        somedata=LanguagesForm(request.POST)
        if somedata.is_valid():
            newdata=somedata.save(commit=False)
            newdata.User_id=sdata.id
            newdata.save()
            return redirect('updatelang',sdata.id)  

def deletelang(request,pk):
    somedata=Languages.objects.get(id=pk)
    somedata.delete()
    return redirect('updatelang',somedata.User_id)

def updateNewlang(request,pk,uid):
    if request.method=='GET':
        somedata=Languages.objects.get(id=pk)
        somedata.delete()
        return render(request,'updatelang.html',{'msg':'update','form':LanguagesForm(instance=somedata)})
    if request.method == 'POST':
        somedata=LanguagesForm(request.POST)
        
        if somedata.is_valid():
            newdata=somedata.save(commit=False)
            newdata.User_id=uid
            newdata.save()
            
        return redirect('updatelang',uid)

def applicants(request, user, jobid):
    try:
        somedata = Personalinfo.objects.get(Name=user)
        if Applicant.objects.filter(Job_id=jobid, seeker_id=somedata.id).exists():
            return render(request, 'success.html', {'error': 'You have already applied for this job.'})
        
        Applicant.objects.create(Job_id=jobid, seeker_id=somedata.id)
        return render(request, 'success.html')

    except Personalinfo.DoesNotExist:
        return render(request, 'success.html', {'error': 'User information not found.'})


def applidjoblist(request,user):
    somedata=Personalinfo.objects.get(Name=user)
    applyjovid=Applicant.objects.filter(seeker_id=somedata.id)
    applyedjobs=[]
    for jobid in applyjovid:
        applyedjobs.append(JobPost.objects.filter(id=jobid.Job_id))
    return render(request,'appliedjobs.html',{'data':applyedjobs})

    
class Addskills(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'updatedskills.html', {'msg': 'add', 'form': SkillForm()})
    def post(self,request,*args, **kwargs):
        somedata=SkillForm(request.POST)
        if somedata.is_valid():
            newdata=somedata.save(commit=False)
            userdata=Personalinfo.objects.get(Name=request.user)
            newdata.User_id=userdata.id
            newdata.save()
            s_data=Skill.objects.filter(User_id=userdata.id)
            return redirect('updateskill',userdata.id) 