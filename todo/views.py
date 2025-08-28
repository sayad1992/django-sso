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

def home(request):
    if request.user.is_authenticated:
        return HttpResponse(
            f"""
            Hello {request.user.first_name or request.user.username}, 
            <a href="/tasks/">Go to your tasks</a><br>
            <form action="/logout/" method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">
                <button type="submit" class="btn btn-danger">Logout</button>
            </form>
            """
        )
    else:
        return HttpResponse(
            """
            Welcome! <br>
            <a href="/accounts/login/" class="btn btn-secondary">Login with Username/Password</a><br>
            <a href="/oauth2/login" class="btn btn-primary">Login with ADFS</a>
            """
        )

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "todo/task_list.html", {"tasks": tasks})

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