from django.db import models

class Material(models.Model):
    partida = models.CharField(max_length=50)
    nombre_material = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.partida} - {self.nombre_material}"