from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('inbox/', views.inbox, name='inbox'),
    path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/employer/', views.register_employer, name='register_employer'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
