from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
comment_status= [("pending", "Pending"), ("approved", "Approved")]

# Create your models here.
class Tasks(models.Model):
    # relationships
    assign_by=models.ForeignKey(User,related_name='assigned_by' ,on_delete=models.CASCADE)
    assign_to=models.ForeignKey(User,related_name='assign_to' ,on_delete=models.CASCADE)
    
    # fields
    task_name=models.CharField(max_length=100)
    task_desc=models.CharField(max_length=250)
    status=models.IntegerField(default='')
    # CharField
    # Choices
    
    # timestamps
    start_date=models.DateField(auto_now=True)
    end_date=models.DateField()
    
    def __str__(self):
        return self.task_name
    
class Comments(models.Model):
    #relationship
    task_id = models.ForeignKey(Tasks, related_name='task_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE)
    #fields
    comment = models.TextField(max_length=350)
    com_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=250, choices=comment_status, default="pending")
    
    def __str__(self):
        return self.comment
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image  = models.ImageField(default='default.jpg',upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.first_name} Profile'