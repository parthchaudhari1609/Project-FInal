from django.contrib import admin
from django.urls import path,include
from .import views
from django.contrib.auth.views import LogoutView
from .views import *
urlpatterns = [
    
    path("manager-register/",views.ManagerRegisterView.as_view(),name="manager-register"),
    path("login/",views.UserLoginView.as_view(),name="login"),
    path("manager-dashboard/",views.ManagerDashboradView.as_view(),name="manager-dashboard"),
    path("developer-dashboard/",views.DeveloperDashboradView.as_view(),name="developer-dashboard"),
    path("logout/",LogoutView.as_view(next_page=('login')),name="logout"),
    path("developer-register/",views.DeveloperRegisterView.as_view(),name="developer-register"),
    path('profile/', profile_view, name='profile')
    # path("sendmail/",views.sendMail,name="sendmail"),

]