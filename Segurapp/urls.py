"""Segurapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.contrib import admin as admin
from django.urls import path as path
from django.conf.urls import url as url

from django.contrib.auth import views as auth_views
from controller import viewsController

urlpatterns = [
    path('admin/', admin.site.urls),

    path('index/', viewsController.index,name = 'index'),
    path('mapa/', viewsController.mapa,name = 'mapa'),

	path('signup/', viewsController.signup, name='signup'),
	path('logout/', viewsController.logout, name='logout'),
	path('login/', viewsController.login, name='login'),
	path('', viewsController.home, name='home'),
]
