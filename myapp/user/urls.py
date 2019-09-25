"""week4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

# all the urls are called
urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration),
    path('auth/jwt/', obtain_jwt_token),
    path('auth/jwt/refresh', refresh_jwt_token),
    path('login/', views.login),
    path('login/forgotpassword', views.forgot_password),
    path('activate/<token>/', views.activate, name="activate"),
    path('reset_password/<token>/', views.reset_password, name="reset_password"),
    path('login/forgotpassword/resetpassword/<userReset>', views.resetpassword, name="resetpassword"),
    path('logout/', views.logout),
    path('session/', views.session),



]
