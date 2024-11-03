# forms.py
from django import forms
from .models import Producto, Partida, Categoria, UnidadMedida

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'partida', 'categoria', 'unidad_medida', 'cantidad_disponible', 'estado']

class PartidaForm(forms.ModelForm):
    class Meta:
        model = Partida
        fields = ['nombre', 'descripcion']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = ['nombre']
