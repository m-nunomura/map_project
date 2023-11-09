"""
URL configuration for map_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout_done"),
    path("signup/", views.Signup.as_view(), name="signup"), 
    path("signup_done/", views.SignupDone.as_view(), name="signup_done"), 
    path("my_page/<int:pk>/", views.MyPage.as_view(), name="my_page"),
    path("user_update/<int:pk>", views.UserUpdate.as_view(), name="user_update"),
    path("password_change/", views.PasswordChange.as_view(), name="password_change"), # パスワード変更
    path("password_change_done/", views.PasswordChangeDone.as_view(), name="password_change_done"), # パスワード変更完了
]
