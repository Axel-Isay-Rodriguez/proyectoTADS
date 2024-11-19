from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.utils.decorators import decorator_from_middleware
from django.utils.cache import add_never_cache_headers
from django.middleware.cache import MiddlewareMixin
from .factories import FormFactory  # Importa FormFactory
from inventariosTec.models import PrestamoDetalle
from .models import Prestamo
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PrestamoForm, OrdenTrabajoForm
from .models import Prestamo, OrdenTrabajo
from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from .forms import PrestamoForm, PrestamoDetalleForm, OrdenTrabajoForm
from .models import Prestamo, PrestamoDetalle, Producto
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Prestamo, OrdenTrabajo
from .forms import PrestamoForm, OrdenTrabajoForm
from django.forms import modelformset_factory


class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response

no_cache = decorator_from_middleware(NoCacheMiddleware)

def grupos_usuario(request):
    if request.user.is_authenticated:
        grupos = request.user.groups.values_list('name', flat=True)
    else:
        grupos = []
    return {'user_groups': grupos}

# Formulario de registro
class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Las contraseñas no coinciden.")
        return cleaned_data

def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # Verificar que las contraseñas coinciden
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'register.html')

        # Crear un nuevo usuario
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.save()

            messages.success(request, 'Tu cuenta ha sido creada exitosamente. Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'El nombre de usuario ya existe. Por favor, elige otro.')

    return render(request, 'register.html')

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='Administrador').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Operador').exists():
                return redirect('operador_dashboard')
            elif user.groups.filter(name='Usuario Avanzado').exists():
                return redirect('usuario_avanzado_dashboard')
            elif user.groups.filter(name='Usuario Básico').exists():
                return redirect('usuario_basico_dashboard')
            else:
                return redirect('no_autorizado')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    return render(request, 'login.html')

def home_view(request):
    user_groups = request.user.groups.values_list('name', flat=True) if request.user.is_authenticated else []
    context = {'user_groups': user_groups}
    return render(request, 'home.html', context)

def es_administrador(user):
    return user.groups.filter(name='Administrador').exists()

def es_operador(user):
    return user.groups.filter(name='Operador').exists()

def es_usuario_avanzado(user):
    return user.groups.filter(name='Usuario Avanzado').exists()

def es_usuario_basico(user):
    return user.groups.filter(name='Usuario Básico').exists()

@user_passes_test(es_administrador)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@user_passes_test(es_operador)
def operador_dashboard(request):
    return render(request, 'operador_dashboard.html')

@login_required
@user_passes_test(es_usuario_avanzado)
def usuario_avanzado_dashboard(request):
    return render(request, 'usuario_avanzado_dashboard.html')

@login_required
@user_passes_test(es_usuario_basico)
def usuario_basico_dashboard(request):
    return render(request, 'usuario_basico_dashboard.html')

@login_required
@user_passes_test(es_administrador)
@no_cache
def gestionar_usuarios(request):
    query = request.GET.get('q', '')  # Obtén el término de búsqueda desde la URL
    usuarios = User.objects.filter(Q(username__icontains=query))
    grupos = Group.objects.all()

    if request.method == 'POST':
        # Verifica si se actualiza un grupo
        if 'usuario_id' in request.POST and 'grupo_id' in request.POST:
            usuario_id = request.POST.get('usuario_id')
            grupo_id = request.POST.get('grupo_id')

            usuario = get_object_or_404(User, id=usuario_id)
            grupo = get_object_or_404(Group, id=grupo_id)

            usuario.groups.clear()
            usuario.groups.add(grupo)

            # Agrega el mensaje y redirige
            messages.success(request, f'Grupo actualizado para {usuario.username}')
            return redirect('gestionar_usuarios')

    return render(request, 'gestionar_usuarios.html', {
        'usuarios': usuarios,
        'grupos': grupos,
        'query': query,
    })

@login_required
@user_passes_test(es_administrador)
@no_cache
def gestionar_producto(request, producto_id=None):
    producto = get_object_or_404(Producto, id=producto_id) if producto_id else None

    # Crear formularios usando el FormFactory
    producto_form = FormFactory.create_form('producto', instance=producto)
    partida_form = FormFactory.create_form('partida')
    categoria_form = FormFactory.create_form('categoria')
    unidad_medida_form = FormFactory.create_form('unidad_medida')

    if request.method == 'POST':
        if 'guardar_producto' in request.POST:
            producto_form = FormFactory.create_form('producto', request.POST, instance=producto)
            if producto_form.is_valid():
                producto_form.save()
                messages.success(request, "Producto guardado exitosamente.")
                return redirect('gestionar_producto')

        elif 'guardar_partida' in request.POST:
            partida_form = FormFactory.create_form('partida', request.POST)
            if partida_form.is_valid():
                partida_form.save()
                messages.success(request, "Partida guardada exitosamente.")

        elif 'guardar_categoria' in request.POST:
            categoria_form = FormFactory.create_form('categoria', request.POST)
            if categoria_form.is_valid():
                categoria_form.save()
                messages.success(request, "Categoría guardada exitosamente.")

        elif 'guardar_unidad_medida' in request.POST:
            unidad_medida_form = FormFactory.create_form('unidad_medida', request.POST)
            if unidad_medida_form.is_valid():
                unidad_medida_form.save()
                messages.success(request, "Unidad de medida guardada exitosamente.")

    context = {
        'producto_form': producto_form,
        'partida_form': partida_form,
        'categoria_form': categoria_form,
        'unidad_medida_form': unidad_medida_form,
    }

    return render(request, 'gestionar_producto.html', context)

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

# Vista para acceso denegado
def no_autorizado(request):
    return render(request, 'no_autorizado.html')

@login_required
def mis_prestamos(request):
    # Filtrar los préstamos que pertenecen al usuario actual
    prestamos = Prestamo.objects.filter(usuario=request.user)

    context = {
        'prestamos': prestamos,
    }

    return render(request, 'mis_prestamos.html', context)

@login_required
def lista_prestamos(request):
    # Filtrar los préstamos que pertenecen al usuario actual
    prestamos = Prestamo.objects.filter(usuario=request.user)

    context = {
        'prestamos': prestamos,
    }

    return render(request, 'lista_prestamos.html', context)



@login_required
def crear_prestamo(request):
    PrestamoDetalleFormSet = formset_factory(PrestamoDetalleForm, extra=1)

    # Obtener las órdenes de trabajo no asignadas a ningún préstamo
    ordenes_trabajo = OrdenTrabajo.objects.filter(prestamo__isnull=True)

    if request.method == 'POST':
        prestamo_form = PrestamoForm(request.POST)
        detalle_formset = PrestamoDetalleFormSet(request.POST)
        orden_form = OrdenTrabajoForm(request.POST)
        orden_trabajo_existente_id = request.POST.get('orden_trabajo_existente')

        if prestamo_form.is_valid() and detalle_formset.is_valid():
            prestamo = prestamo_form.save(commit=False)
            detalles_validos = True
            cantidades_temporales = {}

            # Verificar existencias sin modificar la cantidad disponible
            for detalle_form in detalle_formset:
                producto = detalle_form.cleaned_data.get('producto')
                cantidad = detalle_form.cleaned_data.get('cantidad')

                if producto and cantidad:
                    if producto.id not in cantidades_temporales:
                        cantidades_temporales[producto.id] = producto.cantidad_disponible

                    # Verificar si hay suficiente inventario disponible
                    if cantidades_temporales[producto.id] < cantidad:
                        detalle_form.add_error('cantidad', 'No hay suficientes unidades disponibles.')
                        detalles_validos = False
                    else:
                        # Reducir la cantidad temporalmente para la verificación posterior
                        cantidades_temporales[producto.id] -= cantidad

            # Solo si todos los detalles son válidos guardamos el préstamo y sus detalles
            if detalles_validos:
                with transaction.atomic():
                    prestamo.save()

                    # Asignar orden de trabajo existente si se ha seleccionado
                    if orden_trabajo_existente_id:
                        orden_trabajo = OrdenTrabajo.objects.get(id=orden_trabajo_existente_id)
                        prestamo.orden_trabajo = orden_trabajo
                    # Crear orden de trabajo si se ha ingresado información válida y no se seleccionó una existente
                    elif orden_form.is_valid() and (orden_form.cleaned_data.get('lugar') or orden_form.cleaned_data.get('tipo_trabajo')):
                        orden_trabajo = orden_form.save()
                        prestamo.orden_trabajo = orden_trabajo

                    prestamo.save()

                    for detalle_form in detalle_formset:
                        producto = detalle_form.cleaned_data.get('producto')
                        cantidad = detalle_form.cleaned_data.get('cantidad')

                        if producto and cantidad:
                            # Crear el detalle del préstamo
                            PrestamoDetalle.objects.create(
                                prestamo=prestamo,
                                producto=producto,
                                cantidad=cantidad
                            )
                            # Actualizar la cantidad disponible del producto
                            producto.cantidad_disponible = cantidades_temporales[producto.id]
                            producto.save()

                return redirect('admin_dashboard')

    else:
        prestamo_form = PrestamoForm()
        detalle_formset = PrestamoDetalleFormSet()
        orden_form = OrdenTrabajoForm()

    context = {
        'prestamo_form': prestamo_form,
        'detalle_formset': detalle_formset,
        'orden_form': orden_form,
        'ordenes_trabajo': ordenes_trabajo,
    }

    return render(request, 'crear_prestamo.html', context)

@login_required
def listar_prestamos_ordenes(request):
    prestamos = Prestamo.objects.all()
    ordenes = OrdenTrabajo.objects.all()

    context = {
        'prestamos': prestamos,
        'ordenes': ordenes,
    }

    return render(request, 'lista_prestamos_ordenes.html', context)

@login_required
def editar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect('listar_prestamos_ordenes')
    else:
        form = PrestamoForm(instance=prestamo)
    return render(request, 'editar_prestamo.html', {'form': form})

@login_required
def editar_orden_trabajo(request, orden_id):
    orden_trabajo = get_object_or_404(OrdenTrabajo, id=orden_id)

    if request.method == 'POST':
        orden_form = OrdenTrabajoForm(request.POST, instance=orden_trabajo)

        if orden_form.is_valid():
            orden_form.save()
            return redirect('listar_prestamos_ordenes')
    else:
        orden_form = OrdenTrabajoForm(instance=orden_trabajo)

    context = {
        'orden_form': orden_form,
    }

    return render(request, 'editar_orden_trabajo.html', context)
@login_required
def editar_prestamo_completo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    PrestamoDetalleFormSet = modelformset_factory(PrestamoDetalle, form=PrestamoDetalleForm, extra=0, can_delete=True)

    # Crear un formulario para la orden de trabajo si ya existe
    orden_trabajo_form = None
    if prestamo.orden_trabajo:
        orden_trabajo_form = OrdenTrabajoForm(instance=prestamo.orden_trabajo)

    if request.method == 'POST':
        prestamo_form = PrestamoForm(request.POST, instance=prestamo)
        detalle_formset = PrestamoDetalleFormSet(request.POST, queryset=PrestamoDetalle.objects.filter(prestamo=prestamo))

        # Si existe una orden de trabajo asociada, también obtener el formulario actualizado
        if prestamo.orden_trabajo:
            orden_trabajo_form = OrdenTrabajoForm(request.POST, instance=prestamo.orden_trabajo)

        if prestamo_form.is_valid() and detalle_formset.is_valid() and (not orden_trabajo_form or orden_trabajo_form.is_valid()):
            prestamo_form.save()

            # Guardar la orden de trabajo si existe
            if orden_trabajo_form:
                orden_trabajo_form.save()

            detalles = detalle_formset.save(commit=False)

            # Recorre cada detalle del préstamo
            for detalle in detalles:
                producto = detalle.producto

                # Reversa la cantidad antes de actualizarla para recalcular correctamente
                if detalle.pk:
                    detalle_antiguo = PrestamoDetalle.objects.get(pk=detalle.pk)
                    producto.cantidad_disponible += detalle_antiguo.cantidad
                    producto.save()

                # Si se mantiene prestado o regresado/consumido, ajustar la cantidad
                if detalle.estado == 'prestado':
                    producto.cantidad_disponible -= detalle.cantidad
                elif detalle.estado in ['regresado', 'consumido']:
                    producto.cantidad_disponible += detalle.cantidad

                producto.save()
                detalle.save()

            # Eliminar los detalles marcados como eliminados en el formset
            for deleted_detalle in detalle_formset.deleted_objects:
                deleted_detalle.producto.cantidad_disponible += deleted_detalle.cantidad
                deleted_detalle.producto.save()
                deleted_detalle.delete()

            return redirect('listar_prestamos_ordenes')
    else:
        prestamo_form = PrestamoForm(instance=prestamo)
        detalle_formset = PrestamoDetalleFormSet(queryset=PrestamoDetalle.objects.filter(prestamo=prestamo))
    
    context = {
        'prestamo_form': prestamo_form,
        'detalle_formset': detalle_formset,
        'orden_trabajo_form': orden_trabajo_form,
    }

    return render(request, 'editar_prestamo_completo.html', context)

def historial_prestamos(request):
    # Si el usuario es administrador, mostrar todos los préstamos
    if request.user.groups.filter(name='Administrador').exists():
        prestamos = Prestamo.objects.all()
    else:
        # Para otros usuarios, mostrar solo sus préstamos
        prestamos = Prestamo.objects.filter(usuario=request.user)
    
    context = {
        'prestamos': prestamos,
    }
    
    return render(request, 'historial_prestamos.html', context)
@login_required
def ver_prestamo(request, prestamo_id):
    # Obtiene el préstamo específico o retorna un 404 si no existe
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    # Si el usuario no es administrador y no es el dueño del préstamo, redirigir a no autorizado
    if not request.user.groups.filter(name='Administrador').exists() and prestamo.usuario != request.user:
        return render(request, 'no_autorizado.html')
    
    context = {
        'prestamo': prestamo,
        'detalles_prestamo': prestamo.detalles.all(),  # Obtiene todos los detalles del préstamo
        'orden_trabajo': prestamo.orden_trabajo if hasattr(prestamo, 'orden_trabajo') else None,  # Si hay una orden de trabajo asociada
    }
    
    return render(request, 'ver_prestamo.html', context)

@login_required
def ver_ordenes_asignadas(request):
    # Obtiene las órdenes de trabajo asignadas al usuario actual
    ordenes_asignadas = OrdenTrabajo.objects.filter(asignado_a=request.user)

    context = {
        'ordenes_asignadas': ordenes_asignadas,
    }

    return render(request, 'ver_ordenes_asignadas.html', context)

@login_required
def dar_baja_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    
    # Verificar que no intentes eliminarte a ti mismo
    if request.user == usuario:
        messages.error(request, "No puedes eliminarte a ti mismo.")
        return redirect('gestionar_usuarios')

    if request.method == 'POST':
        usuario.delete()  # Eliminar permanentemente al usuario
        messages.success(request, f'Usuario {usuario.username} eliminado exitosamente.')
        return redirect('gestionar_usuarios')