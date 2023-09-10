from django.contrib import admin
from .models import Department,Task, Comments, Profile,CustomUser




# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Task)
admin.site.register(Comments)
admin.site.register(Department)
admin.site.register(Profile)



