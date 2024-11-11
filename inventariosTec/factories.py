# inventariosTec/factories.py

from .forms import ProductoForm, PartidaForm, CategoriaForm, UnidadMedidaForm

class FormFactory:
    @staticmethod
    def create_form(form_type, *args, **kwargs):
        if form_type == 'producto':
            return ProductoForm(*args, **kwargs)
        elif form_type == 'partida':
            return PartidaForm(*args, **kwargs)
        elif form_type == 'categoria':
            return CategoriaForm(*args, **kwargs)
        elif form_type == 'unidad_medida':
            return UnidadMedidaForm(*args, **kwargs)
        else:
            raise ValueError("Tipo de formulario no soportado")