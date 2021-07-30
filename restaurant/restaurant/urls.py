"""restaurant URL Configuration

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
from django.contrib import admin
from django.urls import path
from restrecommender import views as rr
from django.contrib.auth import views as auth_views
from userauthen import views as ua

urlpatterns = [
    path('', rr.home),
    path('admin/', admin.site.urls),
    path('recommender/', rr.recommender_page, name='recommend'),
    path('browse/', rr.browseRest, name='browse'),
    path('home', rr.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', ua.signup, name='signup'),
    path('profile/', rr.profile, name='profile'),
    path('update_item/', rr.updateItem, name='update_item'),
]
