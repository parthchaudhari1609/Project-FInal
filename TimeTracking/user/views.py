from typing import Any
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import User
from .forms import *
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from project.models import Project
from django.contrib.auth import get_user_model
from project.models import UserTask, Task, Project, ProjectModule
import logging


logger = logging.getLogger(__name__)

# Create your views here.
class ManagerRegisterView(CreateView):
    template_name = 'user/manager_register.html'
    model = User
    form_class = ManagerRegistrationForm
    success_url = '/user/login/'
    def form_valid(self,form):
        email = form.cleaned_data.get("email")
        if sendMail(email):
            print("Mail Sent Successfully")
            return super().form_valid(form)
        else:
            return super().form_valid(form)


class DeveloperRegisterView(CreateView):
    template_name = 'user/developer_register.html'
    model = User
    form_class = DeveloperRegistrationForm
    success_url = '/user/login/'
    def form_valid(self,form):
        email = form.cleaned_data.get("email")
        if sendMail(email):
            print("Mail Sent Successfully")
            return super().form_valid(form)
        else:
            return super().form_valid(form)

def sendMail(to):
    subject = "Welcome to TimeTracking"
    message = "Hope You are enjoying your Django Tutorials"
    recepientList = [to]
    EMAIL_FROM = settings.EMAIL_HOST_USER

    send_mail(subject,message,EMAIL_FROM,recepientList)  # attach file # html - search
    return True
    # return HttpResponse('Email Sent')
    
class UserLoginView(LoginView):
    template_name = "user/login.html"
    model = User

    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_manager:
                return "/user/manager-dashboard"
            elif self.request.user.is_developer:
                return "/user/developer-dashboard"

class ManagerDashboradView(ListView):
    template_name = "user/manager_dashboard.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_projects'] = Project.objects.count()
        context['total_modules'] = ProjectModule.objects.count()
        context['total_tasks'] = Task.objects.count()
        context['total_developers'] = User.objects.filter(is_developer=True).count()
        return context
    
   

class DeveloperDashboradView(ListView):
    template_name = "user/developer_dashboard.html"
    context_object_name = 'user_tasks'

    def get_queryset(self):
        # Get all tasks assigned to the current user
        user_tasks = UserTask.objects.filter(user=self.request.user)

        # Organize tasks based on their status
        tasks_by_status = {
            'Not Started': user_tasks.filter(task__status__status_name='Not Started'),
            'In-Progress': user_tasks.filter(task__status__status_name='In-Progress'),
            'Testing': user_tasks.filter(task__status__status_name='Testing'),
            'Complete': user_tasks.filter(task__status__status_name='Complete')
        }

        return tasks_by_status
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_projects'] = Project.objects.count()
        context['total_modules'] = ProjectModule.objects.count()
        context['total_tasks'] = Task.objects.count()
        context['total_developers'] = User.objects.filter(is_developer=True).count()
        return context
    
    

def profile_view(request):
    user_profile = User.objects.get(username=request.user.username)
    return render(request, 'user/profile.html', {'user_profile': user_profile})


