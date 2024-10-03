# inventariosTec/views.py
from django.shortcuts import render, redirect
from .forms import MaterialFormSet

def registrar_materiales(request):
    if request.method == 'POST':
        formset = MaterialFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('home')  # Redirige de vuelta a la página de inicio
    else:
        formset = MaterialFormSet(queryset=None)

    return render(request, 'registrar_materiales.html', {'formset': formset})


def home(request):
    return render(request, 'home.html')