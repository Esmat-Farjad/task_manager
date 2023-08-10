from django.db import models
from django.contrib.auth.models import User

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
    
    