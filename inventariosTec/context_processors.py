# inventariosTec/context_processors.py

from django.contrib.auth.models import Group

def grupos_usuario(request):
    if request.user.is_authenticated:
        grupos = request.user.groups.values_list('name', flat=True)
    else:
        grupos = []
    return {'user_groups': grupos}
