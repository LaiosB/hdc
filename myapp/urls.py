"""
URL configuration for co2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import home, mapa, register, huella, nosotros, perfil
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [ 
    path('', home, name='home'),
    path('mapa/', mapa, name='mapa'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('huella/', huella, name='huella'),
    path('nosotros/', nosotros, name='nosotros'),
    path('perfil/', perfil, name='perfil'),
]

