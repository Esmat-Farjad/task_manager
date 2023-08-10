from datetime import datetime, timedelta, time
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Tasks

# Create your views here.
def Base(request):
    
    return render(request, 'taskmanager/base.html')

def Login(request):
    if request.method=='POST':
        user_name=request.POST['uname']
        pass1=request.POST['pwd']
        user=authenticate(request, username=user_name, password=pass1)
        if user is not None:
            login(request, user)
            fname=user.first_name
            lname=user.last_name
            id=user.id
            flag='all'
            all_tasks=Tasks.objects.filter(assign_to_id=id)
            
            return render(request, 'taskmanager/dashboard.html', {'fname':fname, 'lname':lname, 'flag':flag, 'tasks':all_tasks})
            
        else:
            messages.error(request, ('Invalid Credential !'))
            
    return render(request, 'taskmanager/login.html')
    
def update_tasks(request, task_id):
    st=0
    Tasks.objects.filter(id=task_id).update(status=st)
    user=request.user
    fname=user.first_name
    lname=user.last_name
    id=user.id
    flag='all'
    all_tasks=Tasks.objects.filter(assign_to_id=id) 
    return render(request, 'taskmanager/dashboard.html', {'fname':fname, 'lname':lname, 'flag':flag,'tasks':all_tasks})           
    

def Signup(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        username=request.POST['uname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if pass1 != pass2:
            messages.error(request, ('Password Dose Not Match !'))
        else:
            new_record=User.objects.create_user(first_name=fname, last_name=lname, email=email, username=username, password=pass1)
            new_record.save()
            messages.success(request, ('You have registered successfully !'))
            
    return render(request, 'taskmanager/signup.html')

@login_required(login_url='/taskmanager/login')
def dashboard(request):
    all_tasks=Tasks.objects.all()
    st = -1
    for val in all_tasks:
        if val.end_date < datetime.now().date():
            Tasks.objects.filter(id=val.id).update(status=st)
            
    user=request.user
    fname=user.first_name
    lname=user.last_name
    id=user.id
    flag='all'
    all_tasks=Tasks.objects.filter(assign_to=id)
    return render(request, 'taskmanager/dashboard.html', {'fname':fname, 'lname':lname, 'flag':flag, 'tasks':all_tasks})

@login_required(login_url='/taskmanager/login')
def assign_task(request):
    users=User.objects.all()
    if request.method=='POST':
        taskname=request.POST['taskname']
        task_desc=request.POST['task_desc']
        end_date=request.POST['end_date']
        
        assign_to=request.POST['assign_to']
        assign_by=request.user 
        status=True
        new_record=Tasks(task_name=taskname, task_desc=task_desc, end_date=end_date, assign_to_id=assign_to, assign_by=assign_by, status=status)
        new_record.save()
        messages.success(request, f"Task assigned successfully")
    
    return render(request, 'taskmanager/add_task.html',{'users':users})
    

def Logout(request):
    logout(request)
    return render(request, 'taskmanager/login.html')

# dashboard operations
def active_task(request, sign):
    if sign == 'active':
        user=request.user
        fname=user.first_name
        lname=user.last_name
        id=user.id
        st=1
        flag=sign
        all_tasks=Tasks.objects.filter(assign_to=id,status=st)
    elif sign == 'c_task':
        user=request.user
        fname=user.first_name
        lname=user.last_name
        id=user.id
        st=0
        flag=sign
        all_tasks=Tasks.objects.filter(assign_to=id,status=st)
    elif sign == 'e_task':
        user=request.user
        fname=user.first_name
        lname=user.last_name
        id=user.id
        st= -1
        flag=sign
        all_tasks=Tasks.objects.filter(assign_to=id,status=st)
    elif sign == 'm_task':
        user=request.user
        fname=user.first_name
        lname=user.last_name
        id=user.id
        flag=sign
        all_tasks=Tasks.objects.filter(assign_by=id)
    else:
        user=request.user
        fname=user.first_name
        lname=user.last_name
        id=user.id
        flag=sign
        all_tasks=Tasks.objects.filter(assign_to=id)
    return render(request, 'taskmanager/dashboard.html', {'fname':fname, 'lname':lname, 'flag':flag, 'tasks':all_tasks})
    