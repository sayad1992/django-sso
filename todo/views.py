from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from django.urls import reverse

from django.http import HttpResponse
from django.urls import reverse
from django.middleware.csrf import get_token

from django.http import HttpResponse
from django.middleware.csrf import get_token


def home(request):
    backend = request.session.get('_auth_user_backend', '') if request.user.is_authenticated else ''
    return render(request, "todo/home.html", {"backend": backend})

@login_required
def task_list(request):
    backend_path = request.session.get('_auth_user_backend', None)
    is_sso = False

    if backend_path and "AdfsAuthCodeBackend" in backend_path:
        is_sso = True

    tasks = Task.objects.filter(user=request.user)
    return render(request, "todo/task_list.html", {
        "tasks": tasks,
        "is_sso": is_sso,  
    })

@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Task.objects.create(user=request.user, title=title)
        return redirect("task_list")
    return render(request, "todo/add_task.html")

def sso_logout(request):
    
    logout(request)

    adfs_logout_url = "https://adfs.demo.lab/adfs/oauth2/logout"

    
    params = urlencode({"post_logout_redirect_uri": "https://127.0.0.1:8000/"})
    return redirect("https://adfs.demo.lab/adfs/oauth2/logout")