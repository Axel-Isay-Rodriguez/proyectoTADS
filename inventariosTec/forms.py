# forms.py
from django import forms
from .models import Producto, Partida, Categoria, UnidadMedida
from .models import Prestamo, OrdenTrabajo,PrestamoDetalle

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

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['usuario', 'activo']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }

class PrestamoDetalleForm(forms.ModelForm):
    class Meta:
        model = PrestamoDetalle
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = ['lugar', 'tipo_trabajo', 'descripcion', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'lugar': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_trabajo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }        