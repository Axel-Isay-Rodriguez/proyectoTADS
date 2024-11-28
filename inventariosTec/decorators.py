import logging
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

# Configurar el logger
logger = logging.getLogger(__name__)

def registrar_acceso(func):
    """
    Decorador para registrar accesos a una vista.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger.info(f"Vista '{func.__name__}' accesada por {request.user.username if request.user.is_authenticated else 'un usuario anónimo'}.")
        return func(request, *args, **kwargs)
    return wrapper

def verificar_rol(requerido):
    """
    Decorador para verificar que el usuario pertenece a un rol específico.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user.groups.filter(name=requerido).exists():
                messages.error(request, f"No tienes permiso para acceder a esta vista. Se requiere el rol: {requerido}.")
                return redirect('no_autorizado')
            return func(request, *args, **kwargs)
        return wrapper
    return decorator