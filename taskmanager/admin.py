from django.contrib import admin
from .models import Tasks, Comments, Profile


# Register your models here.
admin.site.register(Tasks)
admin.site.register(Comments)
admin.site.register(Profile)