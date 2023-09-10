from datetime import datetime, timedelta, time

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash
from .models import Task, Comments, Profile, Department
from django.contrib.auth import get_user_model
User=get_user_model()


# Create your views here.
def Base(request):
    
    return render(request, 'taskmanager/base.html')

def home(request):
    task = Task.objects.all().count()
    staff = User.objects.all().count()
    dept = Department.objects.all().count()
    return render(request, 'home.html', {'task':task, 'staff':staff, 'dept':dept})

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
                if user.is_staff:
                    sign = 'allTask'
                    allDataValue = Task.objects.all().order_by('-start_date')
                    return render(request, 'taskmanager/admin.html', {'data':allDataValue,'sign':sign})
                else:
                    id=user.id
                    flag='all'
                    all_tasks=Task.objects.filter(assign_to_id=id).order_by('-start_date')
                    all_comment=Comments.objects.filter(user_id = id)
                    return render(request, 'taskmanager/dashboard.html', {'flag':flag, 'tasks':all_tasks, 'all_comment':all_comment})
                
            else:
                messages.error(request, ('Invalid Credential !'))
    return render(request, 'taskmanager/login.html')            

        
    
def update_tasks(request, task_id, flag):
    
    if flag == 'start':
        st=50
        Task.objects.filter(id=task_id).update(status=st)
        user=request.user
        fname=user.first_name
        lname=user.last_name
        id=user.id
        flag='all'
        all_tasks=Task.objects.filter(assign_to_id=id) 
    elif flag == 'done':
        st=80
        Task.objects.filter(id=task_id).update(status=st)
        user=request.user
        fname=user.first_name
        lname=user.last_name
        id=user.id
        flag='all'
        all_tasks=Task.objects.filter(assign_to_id=id).order_by('-start_date')
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
        dept = request.POST['dept']
        if pass1 != pass2:
            messages.error(request, ('Password Dose Not Match !'))
        else:
            new_record=User.objects.create_user(first_name=fname, last_name=lname, email=email, username=username, password=pass1, department_id=dept, is_active=False)
            new_record.save()
            messages.success(request, ('You have registered successfully !'))
            return render(request, 'taskmanager/not_active.html')
    departments = Department.objects.all()
    return render(request, 'taskmanager/signup.html', {'depts':departments})

@login_required(login_url='/taskmanager/login')
def dashboard(request):
    all_tasks=Task.objects.all()
    st = -1
    for val in all_tasks:
        if val.end_date < datetime.now().date():
            Task.objects.filter(id=val.id).update(status=st)
            
    user=request.user
    id=user.id
    flag='all'
    all_comment=Comments.objects.filter(user_id = id)
    all_tasks=Task.objects.filter(assign_to=id).order_by("-start_date")
    return render(request, 'taskmanager/dashboard.html', {'flag':flag, 'tasks':all_tasks, 'all_comment':all_comment})

@login_required(login_url='/taskmanager/login')
def assign_task(request):
    users=User.objects.all()
    if request.method=='POST':
        taskname=request.POST['taskname']
        task_desc=request.POST['task_desc']
        end_date=request.POST['end_date']
        
        assign_to=request.POST['assign_to']
        user = User.objects.select_related('department').get(pk=assign_to)        
        dept=user.department.id
        assign_by=request.user 
        status=True
        new_record=Task(task_name=taskname, task_desc=task_desc, end_date=end_date, assign_to_id=assign_to,dept_id=dept, assign_by=assign_by, status=status)
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
        id=user.id
        st=1
        flag=sign
        all_tasks=Task.objects.filter(assign_to=id,status=st)
    elif sign == 'c_task':
        user=request.user
        id=user.id
        st=100
        flag=sign
        all_tasks=Task.objects.filter(assign_to=id,status=st)
    elif sign == 'e_task':
        user=request.user
        id=user.id
        st= -1
        flag=sign
        all_tasks=Task.objects.filter(assign_to=id,status=st)
    elif sign == 'm_task':
        user=request.user
        id=user.id
        flag=sign
        all_tasks=Task.objects.filter(assign_by=id)
    else:
        user=request.user
        id=user.id
        flag=sign
        all_tasks=Task.objects.filter(assign_to=id).order_by('-start_date')
    all_comment=Comments.objects.filter(user_id = request.user.id)
    return render(request, 'taskmanager/dashboard.html', {'flag':flag, 'tasks':all_tasks, 'all_comment':all_comment})

# user profile page 
@login_required(login_url='/taskmanager/login')
def user_profile(request,userID):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        username=request.POST['username']
        userId=userID

        User.objects.filter(id=userId).update(first_name=fname, last_name=lname, email=email, username=username)
        if len(request.FILES) != 0:
            profile_image=request.FILES['image']
            new_record=Profile(user_id=userId, image=profile_image)
            new_record.save()
        
    current_user=User.objects.get(pk=userID)
    # current_user=User.objects.filter(id=userID).select_related('profile')
    m_task=Task.objects.filter(assign_to_id=request.user.id, status=100).count()
    # day=datetime.now()
    # today=day.strftime('%A')
    print(current_user)
    return render(request, 'taskmanager/user_profile.html', {'c_user':current_user, 'No_task':m_task})


@login_required(login_url='/taskmanager/login')
def task_evaluate(request, tid):
    flag='all'
    comp_task=Task.objects.filter(id=tid)
    return render(request, 'taskmanager/task_evaluate.html',{'comp_task':comp_task, 'flag':flag})

@login_required(login_url='/taskmanager/login')
def evaluation(request, tid, flag):
    
    if flag == 'RT':
        key = 'RT'
    elif flag == 'CT':
        key = 'CT'
    else:
        key = 'all'
        
    comp_task=Task.objects.filter(id=tid)
    if request.method == 'POST':
        task_name=request.POST['task_name']
        task_desc=request.POST['task_desc']
        end_date=request.POST['end_date']
        index=request.POST['task_id']
        st = 1
        Task.objects.filter(id = index).update(task_name = task_name, task_desc = task_desc, end_date = end_date, status = st)
        messages.success(request, "The Task Re-assigned Successfully !")
    return render(request, 'taskmanager/task_evaluate.html',{'comp_task':comp_task,'flag':key})

@login_required(login_url='/taskmanager/login')
def Commenting(request, userId, taskId):
    
    if request.method == 'POST':
        task_id=taskId
        user_id=userId
        comment_text=request.POST['comment']
        st=100
        flag = 'all'
        Task.objects.filter(id = task_id).update(status= st)
        new_record= Comments(comment = comment_text, task_id = task_id, user_id = user_id,)
        new_record.save()
        messages.success(request, "The Task Confirmed Successfully !")
        return redirect('taskmanager:evaluation', tid=task_id, flag=flag)
  
@login_required(login_url='/taskmanager/login')
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

@login_required(login_url='/taskmanager/login')
def adminDashboard(request):
    if request.method == 'POST':
        dept_head = request.POST['dept_head']
        dept_name = request.POST['dept_name']
        dept_desc = request.POST['dept_desc']
        operation = request.POST['operation']
        did = request.POST['deptID']
        if operation:
            Department.objects.filter(id = did).update(dept_head = dept_head, department = dept_name, Description = dept_desc)
            messages.success(request, "Department Updated Successfully.")
        else:
            new_record = Department(dept_head = dept_head, department = dept_name, Description = dept_desc)
            new_record.save()
            messages.success(request, "Department Added Successfully...")
   
    allDeptartment = Department.objects.all()
    sign = 'allDept'
    member = Department.objects.annotate(num_user=Count('customuser'))
    return render (request, 'taskmanager/admin.html', {'data':allDeptartment, 'sign':sign, 'no_stuff':member})


def adminRoute(request, flag):
    sign = 'allData'
    allDataValue = ''
    member = User.objects.all().count()
    dept_list = ''
    task_count = Task.objects.all().count()
    d_list = Department.objects.all().count()
    progress = Task.objects.filter(status = 50).count()
    waiting = Task.objects.filter(status = 80).count()
    expire = Task.objects.filter(status = -1).count()
    active = Task.objects.filter(status = 1).count()
    comp = Task.objects.filter(status = 100).count()
    dept_task = Department.objects.annotate(task_count=Count('task'))
    print(dept_task.values_list())
    job = {'pro': progress,
           'wait':waiting,
           'exp':expire,
           'active': active,
           'comp':comp,
           'd_list':d_list,
           'user_count':member,
           'task_count':task_count}
    if flag  == 'allTask':
        sign = flag
        dept_list = Department.objects.all()
        allDataValue = Task.objects.all().order_by('-start_date')  
    elif flag == 'allStuff':
        sign = flag
        allDataValue =User.objects.all()
    elif flag == 'allDept':
        sign = flag
        allDataValue = Department.objects.all()
        member = Department.objects.annotate(num_user=Count('customuser'))
    elif flag == 'allData':
        sign = flag
        allDataValue = Task.objects.all().count()
        member = User.objects.all().count()
        dept_list = Department.objects.all().count()
  
    return render(request, 'taskmanager/admin.html', {'data':allDataValue,'sign':sign, 'no_stuff':member,'dept_list':dept_list,'job':job})

def manageTask(request, tid, flag):
    if tid and flag:
        if flag == 'Remove':
            Task.objects.filter(id=tid).delete()
            allDataValue=Task.objects.all().order_by('-start_date')
            messages.success(request, "Task Removed Successfully !")
            sign='allTask'
            dept_list = Department.objects.all()
            return render(request, 'taskmanager/admin.html', {'data':allDataValue,'sign':sign, 'dept_list':dept_list})
        elif flag == 'edit':
            flag='RT'
            com_task= Task.objects.filter(id = tid)
            dept_list = Department.objects.all()
            return render(request, 'taskmanager/task_evaluate.html', {'comp_task':com_task,'flag':flag,'dept_list':dept_list})
        
        
def manageDept(request, did, flag):
    if did and flag:
        if flag == 'edit':
            temp = Department.objects.filter(id = did)
            op = 'update'
            sign = 'allDept'
            
            allDataValue = Department.objects.all()
            member = Department.objects.annotate(num_user=Count('customuser'))
            return render(request, 'taskmanager/admin.html', {'temp':temp, 'op':op,'sign':sign,'data':allDataValue, 'no_stuff':member})
        elif flag == 'Remove':
            Department.objects.filter(id = did).delete()
            sign = 'allDept'
            
            allDataValue = Department.objects.all()
            member = Department.objects.annotate(num_user=Count('customuser'))
            messages.success(request, "Department Removed Successfully.")
            return render(request, 'taskmanager/admin.html', {'sign':sign,'data':allDataValue, 'no_stuff':member})
        
        
def approval(request, index):
    if index:
        User.objects.filter(id = index).update(is_active = True)
        allDataValue= User.objects.all()
        sign = 'allStuff'
        return render(request, 'taskmanager/admin.html', {'data':allDataValue,'sign':sign})

def deleteUser(request, sid):
    if sid:
        uid = sid
        User.objects.filter(id = uid).delete()
        messages.success(request, "The Stuff deleted successfully !")
        allDataValue =User.objects.all()
        sign = 'allStuff'
        return render(request, 'taskmanager/admin.html', {'data':allDataValue,'sign':sign})

def searchUser(request):
    if request.method == 'POST':
        s_name = request.POST['stuff']
        data = User.objects.filter(first_name = s_name)
        if data:
            sign = 'allStuff'
            return render(request, 'taskmanager/admin.html', {'data':data,'sign':sign})
        else: 
            messages.error(request, "Oops.. ! User dose not exist !")
            data = User.objects.all()
            sign = 'allStuff'
            return render(request, 'taskmanager/admin.html', {'data':data,'sign':sign})
        
def searchTask(request):
    if request.method == 'POST':
        task_title = request.POST['task_title']
        data = Task.objects.filter(task_name = task_title)
        if data:
            sign = 'allTask'
            return render(request, 'taskmanager/admin.html', {'sign':sign, 'data':data})
        else:
            messages.error(request, "Oops...! Tasks not found !")
            data = Task.objects.all().order_by('-start_date')
            sign = 'allTask'
            return render(request, 'taskmanager/admin.html',{'data':data, 'sign':sign})
        
        
def getDetails(request, sid):
    if sid:
        d = Department.objects.get(id = sid)
        u = User.objects.filter(department_id = sid)
      
        return render(request, 'taskmanager/dept_details.html',{'stuff':u})
    
def appliedFilter(request):
    if request.method == 'POST':
        tid = request.POST['department']
        sign='allStuff'
        dept_list = Department.objects.all()
        allDataValue = User.objects.filter(department_id = tid)
        f= Department.objects.values('Description').filter(id = tid)
        
        return render(request, 'taskmanager/admin.html', {'data':allDataValue,'sign':sign, 'dept_list':dept_list, 'filterMessage':f})
        