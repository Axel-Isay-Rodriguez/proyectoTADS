from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Partida(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre



class Producto(models.Model):
    ESTADO_CHOICES = [
        ('bueno', 'Bueno'),
        ('malo', 'Malo'),
        ('regular', 'Regular'),
        ('sin_estado', 'Sin Estado'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    partida = models.ForeignKey('Partida', on_delete=models.CASCADE)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey('UnidadMedida', on_delete=models.CASCADE)
    cantidad_disponible = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='sin_estado')  # Nuevo campo

    def __str__(self):
        return self.nombre


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class OrdenTrabajo(models.Model):
    ESTADO_CHOICES = [
        ('sin_asignar', 'Sin Asignar'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado'),
        ('truncada', 'Truncada'),
    ]

    lugar = models.CharField(max_length=100)
    tipo_trabajo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField(default=timezone.now)  # Fecha de inicio con valor predeterminado de hoy
    fecha_fin = models.DateField(blank=True, null=True)  # Fecha de finalización opcional
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='sin_asignar')  # Nuevo campo de estado

    def __str__(self):
        return f"{self.tipo_trabajo} - {self.lugar}"


class Prestamo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    orden_trabajo = models.ForeignKey('OrdenTrabajo', on_delete=models.SET_NULL, blank=True, null=True)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)  # Campo para indicar si el préstamo está activo

    def __str__(self):
        return f"Préstamo de {self.usuario.username} - {self.fecha_prestamo}"

class PrestamoDetalle(models.Model):
    ESTADO_CHOICES = [
        ('prestado', 'Prestado'),
        ('regresado', 'Regresado'),
        ('consumido', 'Consumido'),
    ]

    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='prestado')  # Campo de estado

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} en préstamo {self.prestamo.id}"

    def save(self, *args, **kwargs):
        # Llama al método save() original para guardar el estado
        super().save(*args, **kwargs)
        # Verifica si todos los detalles del préstamo están en "regresado" o "consumido"
        if not self.prestamo.detalles.filter(~Q(estado='regresado') & ~Q(estado='consumido')).exists():
            # Si todos los detalles están en "regresado" o "consumido", desactiva el préstamo
            self.prestamo.activo = False
            self.prestamo.save()