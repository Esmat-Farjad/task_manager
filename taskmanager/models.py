from django.db import models
from django.contrib.auth.models import AbstractUser



comment_status= [("pending", "Pending"), ("approved", "Approved")]

# Create your models here.
class CustomUser(AbstractUser):
    department=models.ForeignKey("Department",on_delete=models.CASCADE,null=True,blank=True)
    
   
    def __str__(self):
        return self.username
    
        
        

class Department(models.Model):
    name = models.CharField(max_length=250)
    Description = models.TextField(max_length=300)
    dept_head = models.CharField(max_length=100)
   
    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('not started','not started'),
        ('in progress','in progress'),
        ('done','done'),
    ]
    # relationships
    assign_by=models.ForeignKey(CustomUser,related_name='assigned_by',on_delete=models.CASCADE)
    assign_to=models.ForeignKey(CustomUser,related_name='assigned_to' ,on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    
    # fields
    task_name=models.CharField(max_length=100)
    task_desc=models.CharField(max_length=250)
    
    status=models.IntegerField(default="not started", choices=STATUS_CHOICES)
    # CharField
    # Choices
    
    # timestamps
    start_date=models.DateField(auto_now=True)
    end_date=models.DateField()
    
    def __str__(self):
        return self.task_name
    
class Comments(models.Model):
    #relationship
    task = models.ForeignKey(Task, related_name='task', on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(CustomUser, related_name='user', on_delete=models.CASCADE,null=True)
    #fields
    comment = models.TextField(max_length=350)
    com_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=250, choices=comment_status, default="pending")
    
    def __str__(self):
        return self.comment
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    
    def __str__(self):
        return self.profile_image
    
class Query(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    text_message = models.TextField(max_length=250)
    data_sent = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.fullname