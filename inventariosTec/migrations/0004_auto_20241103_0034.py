# Generated by Django 5.1.1 on 2024-11-03 07:34
from django.db import migrations

def crear_grupos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Crear grupos
    administrador, _ = Group.objects.get_or_create(name='Administrador')
    operador, _ = Group.objects.get_or_create(name='Operador')
    usuario_avanzado, _ = Group.objects.get_or_create(name='Usuario Avanzado')
    usuario_basico, _ = Group.objects.get_or_create(name='Usuario Básico')

    # Asignar permisos
    permisos_administrador = Permission.objects.all()
    permisos_operador = Permission.objects.filter(codename__in=['add_ordentrabajo', 'change_ordentrabajo', 'view_ordentrabajo', 'add_prestamo', 'change_prestamo', 'view_prestamo'])
    permisos_usuario_avanzado = Permission.objects.filter(codename__in=['view_ordentrabajo', 'view_prestamo'])
    permisos_usuario_basico = Permission.objects.filter(codename__in=['view_prestamo'])

    administrador.permissions.set(permisos_administrador)
    operador.permissions.set(permisos_operador)
    usuario_avanzado.permissions.set(permisos_usuario_avanzado)
    usuario_basico.permissions.set(permisos_usuario_basico)

class Migration(migrations.Migration):

    dependencies = [
        ('inventariosTec', '0003_ordentrabajo_estado'),
    ]

    operations = [
          migrations.RunPython(crear_grupos),
    ]