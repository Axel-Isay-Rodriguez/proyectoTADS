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
from .forms import ProductoForm, PartidaForm, CategoriaForm, UnidadMedidaForm
from .models import Producto
from django.contrib.auth.models import Group
from django.db import models
from inventariosTec.models import PrestamoDetalle

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

def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Asignar al grupo "Usuario Básico"
            grupo_basico = Group.objects.get(name='Usuario Básico')
            user.groups.add(grupo_basico)

            # Autenticar y redirigir al usuario
            login(request, user)
            messages.success(request, "Registro exitoso. Bienvenido!")
            return redirect('home')  # Redirige a la página principal o a la página que desees
    else:
        form = RegistroForm()
    return render(request, 'register.html', {'form': form})
def home(request):
    return render(request, 'home.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirigir según el grupo del usuario
            if user.groups.filter(name='Administrador').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Operador').exists():
                return redirect('operador_dashboard')
            elif user.groups.filter(name='Usuario Avanzado').exists():
                return redirect('usuario_avanzado_dashboard')
            elif user.groups.filter(name='Usuario Básico').exists():
                return redirect('usuario_basico_dashboard')
            else:
                # Si el usuario no pertenece a ningún grupo
                return redirect('no_autorizado')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    return render(request, 'login.html')

def home_view(request):
    user_groups = request.user.groups.values_list('name', flat=True) if request.user.is_authenticated else []
    
    context = {
        'user_groups': user_groups
    }
    
    return render(request, 'home.html', context) # Asegúrate de tener un archivo home.html en tu carpeta de plantillas


def es_administrador(user):
    return user.groups.filter(name='Administrador').exists()

def es_operador(user):
    return user.groups.filter(name='Operador').exists()

@user_passes_test(es_administrador)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')  # Vista solo para administradores

@user_passes_test(es_operador)
def operador_dashboard(request):
    return render(request, 'operador_dashboard.html')  # Vista solo para operadores


@user_passes_test(es_administrador, login_url='no_autorizado')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Otros decoradores según el grupo que desees verificar
def es_usuario_avanzado(user):
    return user.groups.filter(name='Usuario Avanzado').exists()

# Vista para el panel del usuario avanzado
@login_required
@user_passes_test(es_usuario_avanzado)
def usuario_avanzado_dashboard(request):
    return render(request, 'usuario_avanzado_dashboard.html')

def es_usuario_basico(user):
    return user.groups.filter(name='Usuario Básico').exists()

# Vista para el panel del usuario básico
@login_required
@user_passes_test(es_usuario_basico)
def usuario_basico_dashboard(request):
    return render(request, 'usuario_basico_dashboard.html')

def no_autorizado(request):
    return render(request, 'no_autorizado.html')

from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def operador_dashboard(request):
    return render(request, 'operador_dashboard.html')

@login_required
def usuario_avanzado_dashboard(request):
    return render(request, 'usuario_avanzado_dashboard.html')

@login_required
def usuario_basico_dashboard(request):
    return render(request, 'usuario_basico_dashboard.html')

def es_administrador(user):
    return user.groups.filter(name='Administrador').exists()

@login_required
@user_passes_test(es_administrador)
def admin_dashboard(request):
    # Obtener usuarios sin grupo asignado
    usuarios_sin_grupo = User.objects.filter(groups__isnull=True)
    
    return render(request, 'admin_dashboard.html', {
        'usuarios_sin_grupo': usuarios_sin_grupo
    })

def es_administrador(user):
    return user.groups.filter(name='Administrador').exists()

@login_required
@user_passes_test(es_administrador)
@no_cache
def gestionar_usuarios(request):
    usuarios = User.objects.all()
    grupos = Group.objects.all()

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        grupo_id = request.POST.get('grupo_id')

        usuario = get_object_or_404(User, id=usuario_id)
        grupo = get_object_or_404(Group, id=grupo_id)

        # Asigna el grupo seleccionado al usuario (puedes limpiar los grupos existentes si quieres que solo tenga uno)
        usuario.groups.clear()  # Elimina todos los grupos del usuario antes de asignar el nuevo
        usuario.groups.add(grupo)

        messages.success(request, f'Grupo actualizado para {usuario.username}')
        return redirect('gestionar_usuarios')

    return render(request, 'gestionar_usuarios.html', {'usuarios': usuarios, 'grupos': grupos})

@no_cache
def gestionar_usuarios(request):
    grupos = Group.objects.all()
    query = request.GET.get('q')  # Captura el término de búsqueda
    sort = request.GET.get('sort')  # Captura el criterio de ordenación

    # Búsqueda de usuarios
    if query:
        usuarios = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
    else:
        usuarios = User.objects.all()

    # Ordenar usuarios si se ha seleccionado un criterio de ordenación
    if sort in ['username', 'email']:
        usuarios = usuarios.order_by(sort)

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        grupo_id = request.POST.get('grupo_id')

        usuario = get_object_or_404(User, id=usuario_id)
        grupo = get_object_or_404(Group, id=grupo_id)

        # Asignar grupo al usuario
        usuario.groups.clear()  # Elimina los grupos existentes
        usuario.groups.add(grupo)

        messages.success(request, f'Grupo actualizado para {usuario.username}')
        return redirect('gestionar_usuarios')

    return render(request, 'gestionar_usuarios.html', {'usuarios': usuarios, 'grupos': grupos})

def es_administrador(user):
    return user.groups.filter(name='Administrador').exists()

@login_required
@user_passes_test(es_administrador)
@no_cache
def gestionar_usuarios(request):
    grupos = Group.objects.all()
    query = request.GET.get('q')  # Captura el término de búsqueda desde el formulario

    if query:
        usuarios = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
    else:
        usuarios = User.objects.all()

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        grupo_id = request.POST.get('grupo_id')

        usuario = get_object_or_404(User, id=usuario_id)
        grupo = get_object_or_404(Group, id=grupo_id)

        # Asigna el grupo seleccionado al usuario
        usuario.groups.clear()  # Elimina todos los grupos del usuario antes de asignar el nuevo
        usuario.groups.add(grupo)

        messages.success(request, f'Grupo actualizado para {usuario.username}')
        return redirect('gestionar_usuarios')

    return render(request, 'gestionar_usuarios.html', {'usuarios': usuarios, 'grupos': grupos})
@login_required
@user_passes_test(es_administrador)
def gestionar_producto(request, producto_id=None):
    producto = get_object_or_404(Producto, id=producto_id) if producto_id else None

    # Inicializa todos los formularios para que estén listos para usar en la plantilla
    producto_form = ProductoForm(instance=producto)
    partida_form = PartidaForm()
    categoria_form = CategoriaForm()
    unidad_medida_form = UnidadMedidaForm()

    if request.method == 'POST':
        # Identifica cuál formulario se está enviando por el nombre del botón
        if 'guardar_producto' in request.POST:
            producto_form = ProductoForm(request.POST, instance=producto)
            if producto_form.is_valid():
                producto_form.save()
                return redirect('gestionar_producto')  # Redirige después de guardar el producto para evitar reenvío duplicado

        elif 'guardar_partida' in request.POST:
            partida_form = PartidaForm(request.POST)
            if partida_form.is_valid():
                partida_form.save()

        elif 'guardar_categoria' in request.POST:
            categoria_form = CategoriaForm(request.POST)
            if categoria_form.is_valid():
                categoria_form.save()

        elif 'guardar_unidad_medida' in request.POST:
            unidad_medida_form = UnidadMedidaForm(request.POST)
            if unidad_medida_form.is_valid():
                unidad_medida_form.save()

    # Renderiza los formularios con el contexto adecuado
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


