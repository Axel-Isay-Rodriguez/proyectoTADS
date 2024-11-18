from django import forms
from .models import Producto, Partida, Categoria, UnidadMedida

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'partida', 'categoria', 'unidad_medida', 'cantidad_disponible', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Ejemplo: Pluma',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Ejemplo: Pluma Negra de punto mediano, marca BIC.',
                'maxlength': 300,
            }),
            'partida': forms.Select(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Seleccione la partida correspondiente',
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Seleccione la categoría del producto',
            }),
            'unidad_medida': forms.Select(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Seleccione la unidad de medida',
            }),
            'cantidad_disponible': forms.NumberInput(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Ejemplo: 50',
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Seleccione el estado del producto',
            }),
        }

class PartidaForm(forms.ModelForm):
    class Meta:
        model = Partida
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Nombre de la partida',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Descripción breve de la partida',
                'maxlength': 300,
            }),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Nombre de la categoría',
            }),
        }

class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Nombre de la unidad de medida',
            }),
        }