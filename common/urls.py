
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from .views import home

from community.views import create as create_community

urlpatterns = [

    path('', home, name='home'),
    
    # content creation urls
    path('create/community', create_community)
]
