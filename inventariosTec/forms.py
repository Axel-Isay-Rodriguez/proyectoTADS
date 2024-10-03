# forms.py
from django import forms
from django.forms import modelformset_factory
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['partida', 'nombre_material', 'descripcion', 'cantidad', 'ubicacion']

# Crear un formset que permita múltiples formularios
MaterialFormSet = modelformset_factory(Material, form=MaterialForm, extra=3)  # extra define la cantidad de formularios que se mostrarán inicialmente
