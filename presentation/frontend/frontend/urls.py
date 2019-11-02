
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from main import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("homepage", views.list_all_pets, name="homepage"),
    path("homepage/list_user_pets", views.list_user_pets, name="homepage/list_user_pets"),
    path("pet_details/<int:id>", views.show_individual_pet_by_id, name="pet_details"),
    path("search", views.search, name="search"),
    path("create_new_pet", views.create_new_pet, name="create_new_pet"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("reset_password", views.reset_password, name="reset_password"),
    path("reset/<str:authenticator>", views.reset, name="reset"),
]

