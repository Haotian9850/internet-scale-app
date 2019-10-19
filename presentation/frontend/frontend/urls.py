"""frontend URL Configuration

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
from django.conf.urls import include, url
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage', views.list_pets, name='homepage'),
    path('pet_details/<str:name>', views.show_individual_pet_by_name, name='pet_details'),
    path('search', views.search, name='search'),
    path('create_new_pet', views.create_new_pet, name='create_new_pet'),
]

