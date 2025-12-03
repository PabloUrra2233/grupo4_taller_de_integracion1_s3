from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Mesa
from .forms import MesaForm
from usuarios.models import Usuario

def is_admin(user):
    return user.is_authenticated and user.rol == Usuario.Rol.ADMIN

@user_passes_test(is_admin)
def lista_mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'mesas/lista.html', {'mesas': mesas})

@user_passes_test(is_admin)
def crear_mesa(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_mesas')
    else:
        form = MesaForm()
    return render(request, 'mesas/form.html', {'form': form, 'titulo': 'Crear Mesa'})

@user_passes_test(is_admin)
def editar_mesa(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            return redirect('lista_mesas')
    else:
        form = MesaForm(instance=mesa)
    return render(request, 'mesas/form.html', {'form': form, 'titulo': 'Editar Mesa'})

@user_passes_test(is_admin)
def eliminar_mesa(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        mesa.delete()
        return redirect('lista_mesas')
    return render(request, 'mesas/eliminar.html', {'mesa': mesa})
