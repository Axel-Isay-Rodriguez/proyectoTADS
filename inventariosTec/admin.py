from django.contrib import admin
from .models import Partida, UnidadMedida, Categoria, Producto, Ubicacion, OrdenTrabajo, Prestamo, PrestamoDetalle

admin.site.register(Partida)
admin.site.register(UnidadMedida)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Ubicacion)
admin.site.register(OrdenTrabajo)
admin.site.register(Prestamo)
admin.site.register(PrestamoDetalle)
