"""
portia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path("admin/", admin.site.urls),
    url("api/v1/users/create", views.create_user),
    url("api/v1/users/(\d+)/get_by_id", views.get_user_by_id),
    url("api/v1/users/(\d+)/update", views.update_user),
    url("api/v1/users/(\d+)/delete", views.delete_user),
    url("api/v1/pets/create", views.create_pet),
    url("api/v1/pets/get_all_pets", views.get_all_pets),
    url("api/v1/pets/get_by_id", views.get_pet_by_id),
    url("api/v1/pets/get_by_user", views.get_pets_by_username),
    url("api/v1/pets/(\d+)/update", views.update_pet),
    url("api/v1/pets/(\d+)/delete", views.delete_pet),
    url("api/v1/login", views.log_in),
    url("api/v1/logout", views.log_out),
    url("api/v1/reset_password", views.reset_password),
    url("api/v1/update_recommendations", views.update_recommendations)
]
