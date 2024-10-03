# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registrar-materiales/', views.registrar_materiales, name='registrar_materiales'),
]