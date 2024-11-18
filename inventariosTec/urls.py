# urls.py

from . import views
from django.contrib import admin
from inventariosTec import views
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.registro_view, name='register'),
    path('', views.home_view, name='home'), 

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('operador_dashboard/', views.operador_dashboard, name='operador_dashboard'),
    path('usuario_avanzado_dashboard/', views.usuario_avanzado_dashboard, name='usuario_avanzado_dashboard'),
    path('usuario_basico_dashboard/', views.usuario_basico_dashboard, name='usuario_basico_dashboard'),
    path('no_autorizado/', views.no_autorizado, name='no_autorizado'),  # Página para acceso denegado
    path('gestionar_usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('gestionar_producto/', views.gestionar_producto, name='gestionar_producto'),
    path('gestionar_producto/<int:producto_id>/', views.gestionar_producto, name='editar_producto'),
    path('mis_prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('lista_productos/', views.lista_productos, name='lista_productos'),  # Nueva ruta para la lista de productos
    path('lista_prestamos/', views.lista_prestamos, name='lista_prestamos'),
    path('crear_prestamo/', views.crear_prestamo, name='crear_prestamo'),
    path('lista_prestamos_ordenes/', views.listar_prestamos_ordenes, name='listar_prestamos_ordenes'),
    path('editar_prestamo/<int:prestamo_id>/', views.editar_prestamo, name='editar_prestamo'),
    path('editar_orden_trabajo/<int:orden_id>/', views.editar_orden_trabajo, name='editar_orden_trabajo'),
    path('lista_prestamos_ordenes/', views.listar_prestamos_ordenes, name='listar_prestamos_ordenes'),
    path('editar_prestamo_completo/<int:prestamo_id>/', views.editar_prestamo_completo, name='editar_prestamo_completo'),
    path('historial_prestamos/', views.historial_prestamos, name='historial_prestamos'),
    path('ver_prestamo/<int:prestamo_id>/', views.ver_prestamo, name='ver_prestamo'),
    path('editar_orden_trabajo/<int:orden_id>/', views.editar_orden_trabajo, name='editar_orden_trabajo'),
    path('ordenes_asignadas/', views.ver_ordenes_asignadas, name='ver_ordenes_asignadas'),

]