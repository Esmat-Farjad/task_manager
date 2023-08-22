from datetime import datetime, timedelta, time
from hashlib import md5
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash
from .models import Tasks, Comments, Profile

# Create your views here.
def Base(request):
    return render(request, 'taskmanager/base.html')
def home(request):
    return render(request, 'home.html')

def Login(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
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
                all_tasks=Tasks.objects.filter(assign_to_id=id).order_by('-end_date')
                all_comment=Comments.objects.filter(user_id = id)
                return render(request, 'taskmanager/dashboard.html', {'fname':fname, 'lname':lname, 'flag':flag, 'tasks':all_tasks, 'all_comment':all_comment})
                
            else:
                messages.error(request, ('Invalid Credential !'))
    return render(request, 'taskmanager/login.html')            

        
    
def update_tasks(request, task_id, flag):
    
    if flag == 'start':
        st=50
        Tasks.objects.filter(id=task_id).update(status=st)
        user=request.user
        fname=user.first_name
        lname=user.last_name
        id=user.id
        flag='all'
        all_tasks=Tasks.objects.filter(assign_to_id=id) 
    elif flag == 'done':
        st=80
        Tasks.objects.filter(id=task_id).update(status=st)
        user=request.user
        fname=user.first_name
        lname=user.last_name
        id=user.id
        flag='all'
        all_tasks=Tasks.objects.filter(assign_to_id=id).order_by('-end_date')
    all_comment=Comments.objects.filter(user_id = request.user.id)
    return render(request, 'taskmanager/dashboard.html', {'fname':fname, 'lname':lname, 'flag':flag,'tasks':all_tasks, 'all_comment':all_comment})           
    

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
    all_comment=Comments.objects.filter(user_id = id)
    all_tasks=Tasks.objects.filter(assign_to=id).order_by("-end_date")
    return render(request, 'taskmanager/dashboard.html', {'fname':fname, 'lname':lname, 'flag':flag, 'tasks':all_tasks, 'all_comment':all_comment})

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
    return render(request, 'home.html')

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
        st=100
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
        all_tasks=Tasks.objects.filter(assign_to=id).order_by('-end_date')
    all_comment=Comments.objects.filter(user_id = request.user.id)
    return render(request, 'taskmanager/dashboard.html', {'fname':fname, 'lname':lname, 'flag':flag, 'tasks':all_tasks, 'all_comment':all_comment})

# user profile page 
@login_required(login_url='/taskmanager/login')
def user_profile(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        username=request.POST['username']
        userId=request.user.id
        

        
        User.objects.filter(id=userId).update(first_name=fname, last_name=lname, email=email, username=username)
        if len(request.FILES) != 0:
            profile_image=request.FILES['image']
            new_record=Profile(user_id=userId, image=profile_image)
            new_record.save()
        
    current_user=User.objects.filter(id=request.user.id)
    m_task=Tasks.objects.filter(assign_to_id=request.user.id, status=100).count()
    # day=datetime.now()
    # today=day.strftime('%A')
    return render(request, 'taskmanager/user_profile.html', {'c_user':current_user, 'No_task':m_task})


@login_required(login_url='/taskmanager/login')
def task_evaluate(request, tid):
    comp_task=Tasks.objects.filter(id=tid)
    return render(request, 'taskmanager/task_evaluate.html',{'comp_task':comp_task})

def evaluation(request, tid, flag):
    if flag == 'RT':
        key = 'RT'
    elif flag == 'CT':
        key = 'CT'
    else:
        key = 'all'
        
    comp_task=Tasks.objects.filter(id=tid)
    if request.method == 'POST':
        task_name=request.POST['task_name']
        task_desc=request.POST['task_desc']
        end_date=request.POST['end_date']
        index=request.POST['task_id']
        st = 1
        Tasks.objects.filter(id = index).update(task_name = task_name, task_desc = task_desc, end_date = end_date, status = st)
        messages.success(request, "The Task Re-assigned Successfully !")
    return render(request, 'taskmanager/task_evaluate.html',{'comp_task':comp_task,'flag':key})

def Commenting(request, userId, taskId):
    
    if request.method == 'POST':
        task_id=taskId
        user_id=userId
        comment_text=request.POST['comment']
        st=100
        flag = 'all'
        Tasks.objects.filter(id = task_id).update(status= st)
        new_record= Comments(comment = comment_text, task_id_id = task_id, user_id_id = user_id,)
        new_record.save()
        messages.success(request, "The Task Confirmed Successfully !")
        return redirect('taskmanager:evaluation', tid=task_id, flag=flag)
  
  
def changePassword(request):
    if request.method == 'POST':
        old=request.POST['old_password']
        new_password=request.POST['new_password']
        conf_pass=request.POST['confirm_pass']
        error = ''
        success = ''
        status = 0
        if update_session_auth_hash(request, request.user.password) == old:
                error= "Password is Incorrect !"
                status = 404
        
        elif old == new_password:
            error = "The new password should not be the same as old !"
            status = 400
        elif new_password != conf_pass:
            error = "The password dose not match !"
            status = 404
        else:
            u=User.objects.get(id=request.user.id)
            u.set_password(new_password)
            u.save()
            success="Your password changed successfully"
            status = 200
    data= {'status': status, 'message':success, 'error':error}
    return JsonResponse(data, safe=False)
          