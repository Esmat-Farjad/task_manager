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
    path('update_tasks/<task_id>/<flag>', views.update_tasks, name='update_tasks'),
    path('active_task/<sign>', views.active_task, name='active_task'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('task_evaluate/<tid>',views.task_evaluate, name='task_evaluate'),
    path('evaluation/<tid>/<flag>',views.evaluation, name="evaluation"),
    path('Commenting/<userId>/<taskId>',views.Commenting, name='Commenting'),
]
