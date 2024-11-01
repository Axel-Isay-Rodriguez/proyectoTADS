# urls.py
from django.urls import path
from . import views
from django.contrib import admin
from inventariosTec import views
from django.urls import path, include

urlpatterns = [
path('', views.home, name='home'),
path('admin/', admin.site.urls),
]
