
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    url('test/get_all_pets', views.get_pet_list),
    url('test/create_pet', views.create_pet),
    url('test/search_pets', views.search_pets),
    url('test/sort_pets', views.sort_pets),
    url('test/login', views.log_in),
    url('test/logout', views.log_out)
]
