from django.urls import path
from . import views

app_name='taskmanager'

urlpatterns = [
    path('',views.Base, name='Base'),
    path('login/', views.Login, name='login'),
    path('signup/', views.Signup, name='signup'),
    path('logout/', views.Logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assign_task/', views.assign_task, name='assign_task'),
    path('update_tasks/<task_id>', views.update_tasks, name='update_tasks'),
    path('active_task/<sign>', views.active_task, name='active_task')
]
