from django.contrib import admin
from django.urls import path

from services.elasticsearch_service import print_consumer_topic

urlpatterns = [
    path('admin/', admin.site.urls),
]

