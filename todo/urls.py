from django.urls import path
from . import views

from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", views.home, name="home"),          
    path("tasks/", views.task_list, name="task_list"), 
    path("tasks/add/", views.add_task, name="add_task"),
   
    path('oauth2/', include('django_auth_adfs.urls')),
    path('logout/', views.sso_logout, name='sso_logout'),
     
    path("accounts/login/", auth_views.LoginView.as_view(template_name="todo/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]

