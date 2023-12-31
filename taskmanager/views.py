from datetime import datetime
import random

from django.http import JsonResponse
from django.shortcuts import redirect, render
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Count
# from django.contrib.auth import update_session_auth_hash
from .models import Query, Task, Comments, Profile, Department
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods

User=get_user_model()


# Create your views here.
def Base(request):
    
    return render(request, 'taskmanager/base.html')

def home(request):
    task = Task.objects.all().count()
    staff = User.objects.all().count()
    dept = Department.objects.all().count()
    data = {
        'num_task':task,
        'num_stuff':staff,
        'num_dept':dept
    }
    return render(request, 'home.html', {'data':data})

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
                return redirect('home')
            else:
                messages.error(request, 'Invalid Credential !')
    return render(request, 'taskmanager/login.html')            

        
@login_required(login_url='/taskmanager/login')
def update_tasks(request, task_id, flag):
    my_user= request.user
    id = my_user.id
    if flag == 'start':
        st=50
        Task.objects.filter(id=task_id).update(status=st)
        # user=request.user
        # fname=user.first_name
        # lname=user.last_name
        
        flag='all'
        all_tasks = Task.objects.select_related('assign_to').filter(assign_to = id)
        # all_tasks=Task.objects.filter(assign_to_id=id) 
    elif flag == 'done':
        st=80
        Task.objects.filter(id=task_id).update(status=st)
        # user=request.user
        # fname=user.first_name
        # lname=user.last_name
        flag='all'
        all_tasks = Task.objects.select_related('assign_to').filter(assign_to = id).order_by('-start_date')
        # all_tasks=Task.objects.filter(assign_to_id=id).order_by('-start_date')
    all_comment=Comments.objects.select_related('task','user').filter(user = id)
  
    return render(request, 'taskmanager/dashboard.html', {'flag':flag,'tasks':all_tasks, 'all_comment':all_comment, 'my_user':my_user})           
    

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
    st = -1
    for val in Task.objects.all():
        if val.end_date < datetime.now().date():
            Task.objects.filter(id=val.id).update(status=st)
            
    my_user = request.user
    id = request.user.id
    flag='all'
    all_comment=Comments.objects.select_related('task','user').filter(user = request.user.id)
    all_tasks=Task.objects.select_related('assign_by').filter(assign_to=id).order_by('-start_date')
    print(all_tasks)
    context = {
        'flag':flag,
        'tasks':all_tasks,
        'all_comments':all_comment,
        'my_user':my_user,
    }
    return render(request, 'taskmanager/dashboard.html', context)

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
        messages.success(request, "Task assigned successfully")
    
    return render(request, 'taskmanager/add_task.html',{'users':users})
    

def Logout(request):
    logout(request)
    return render(request, 'home.html')

# dashboard operations
def active_task(request, sign):
    my_user = request.user
    id = my_user.id
    if sign == 'active':
        st=1
        flag=sign
        all_tasks=Task.objects.select_related('assign_by').filter(assign_to=id,status=st)
    elif sign == 'c_task':
        st=100
        flag=sign
        all_tasks=Task.objects.select_related('assign_by').filter(assign_to=id,status=st)
    elif sign == 'e_task':
        st= -1
        flag=sign
        all_tasks=Task.objects.select_related('assign_by').filter(assign_to=id,status=st)
    elif sign == 'm_task':
        flag=sign
        all_tasks=Task.objects.select_related('assign_by').filter(assign_by=id)
    else:
        flag=sign
        all_tasks=Task.objects.select_related('assign_by').filter(assign_to=id).order_by('-start_date')
    all_comment=Comments.objects.select_related('task','user').filter(user = id)
    return render(request, 'taskmanager/dashboard.html', {'flag':flag, 'tasks':all_tasks, 'all_comment':all_comment,'my_user':my_user})

# user profile page 
@login_required(login_url='/taskmanager/login')
def user_profile(request,userID):
    # uid = userID
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
    return render(request, 'taskmanager/user_profile.html', {'c_user':current_user, 'No_task':m_task})


@login_required(login_url='/taskmanager/login')
def task_evaluate(request, tid):
    flag='all'
    comp_task=Task.objects.select_related('assign_by').filter(id=tid)
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
        flag = 'CT'
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
            Department.objects.filter(id = did).update(dept_head = dept_head, name = dept_name, Description = dept_desc)
            messages.success(request, "Department Updated Successfully.")
        else:
            new_record = Department(dept_head = dept_head, name = dept_name, Description = dept_desc)
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

    job = {'pro': progress,
           'wait':waiting,
           'exp':expire,
           'active': active,
           'comp':comp,
           'd_list':d_list,
           'user_count':member,
           'task_count':task_count,
           }
    if flag  == 'allTask':
        sign = flag
        dept_list = Department.objects.all()
        allDataValue = Task.objects.all().order_by('-start_date')  
    elif flag == 'allStuff':
        sign = flag
        allDataValue =User.objects.all()
        dept_list = Department.objects.all()
    elif flag == 'allDept':
        sign = flag
        allDataValue = Department.objects.all()
        member = Department.objects.annotate(num_user=Count('customuser'))
    elif flag == 'allData':
        sign = flag
        allDataValue = Task.objects.all().count()
        member = User.objects.all().count()
        dept_list = Department.objects.all().count()
    elif flag == 'query':
        sign = flag
        allDataValue = Query.objects.all().order_by('-data_sent')
  
    return render(request, 'taskmanager/admin.html', {'data':allDataValue,'sign':sign, 'no_stuff':member,'dept_list':dept_list,'job':job,'dept_task':dept_task})

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
      
        return render(request, 'taskmanager/dept_details.html',{'stuff':u, 'departmentDetails':d})
    
def appliedFilter(request):
    if request.method == 'POST':
        tid = request.POST['department']
        sign='allStuff'
        dept_list = Department.objects.all()
        allDataValue = User.objects.filter(department_id = tid)
        f= Department.objects.values('Description').filter(id = tid)
        
        return render(request, 'taskmanager/admin.html', {'data':allDataValue,'sign':sign, 'dept_list':dept_list, 'filterMessage':f})

def contact(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        message = request.POST['message']
        new_record = Query(fullname = fullname, email = email, text_message = message)
        new_record.save()
        messages.success(request, "Your message sent to the administrator successfully.")
        return redirect('home')
    



@require_http_methods(["POST"])
def sendEmail(request):
    user_email = request.POST['email']
    subject = "Reset Password"
    check = User.objects.values_list('id').get(email = user_email)

    if check:
        host = "e.farjad456@gmail.com"
        message_content = "Hello this is a testing email from task manager. your confirmation code is:"
        num = random.randint(100000,199999)
        new_word = f'{message_content}{num}'
        send_mail(subject, new_word, host, [user_email])
        # messages.success(request, "A link has been sent your email ")
        status = 200
        success = "Sent Successfully"
        error = "None"
        data = num
        uid = check
        data= {'status': status, 'data':data, 'uid':uid, 'message':success, 'error':error}
        return JsonResponse(data, safe=False)
    else:
        messages.error(request, "Oops...user dose not found.")
        status = 500
        error = "Oops...Some problem occurred"
        success = "Null"
        data = 0
        data= {'status': status, 'data':data, 'message':success, 'error':error}
        return JsonResponse(data, safe=False)
    
@require_http_methods(["POST"])
def verifyOTP(request):
    user_otp = request.POST['user_otp']
    sys_otp = request.POST['sys_otp']
    uid = request.POST['uid']
    if user_otp == sys_otp:
        return render( request, 'taskmanager/reset_password.html', {'user_id':uid})
    else:
        messages.error(request, "You've entered the incorrect OTP")
        return render(request, 'taskmanager/login.html')
    
@require_http_methods(["POST"]) 
def resetPassword(request):
       new = request.POST['new_password']
       conf = request.POST['confirm_password']
       uid = request.POST['uid']
       if new == conf:
           u=User.objects.get(id=uid)
           u.set_password(new)
           u.save()
           messages.success(request, "Your password changed successfully ")
           return render(request, 'taskmanager/login.html')
       else:
           messages.error(request, "the password dose not matched")
           return render(request, "taskmanager/reset_password.html")
 
def privacy_and_policy(request):
    today = datetime.now()
    return render(request, 'taskmanager/privacy_and_policy.html',{'today':today})  
