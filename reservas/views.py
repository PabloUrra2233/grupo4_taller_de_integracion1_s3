from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib import messages
from .models import Reserva
from .forms import ReservaForm
from usuarios.models import Usuario

@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).select_related('mesa').order_by('-fecha_reserva')
    return render(request, 'reservas/lista.html', {'reservas': reservas, 'titulo': 'Mis Reservas'})

@login_required
def todas_reservas(request):
    if request.user.rol != Usuario.Rol.ADMIN:
        return redirect('mis_reservas')
    reservas = Reserva.objects.all().select_related('usuario', 'mesa').order_by('-fecha_reserva')
    return render(request, 'reservas/lista.html', {'reservas': reservas, 'titulo': 'Todas las Reservas'})

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            messages.success(request, 'Reserva creada exitosamente.')
            return redirect('mis_reservas')
    else:
        form = ReservaForm()
    return render(request, 'reservas/form.html', {'form': form, 'titulo': 'Nueva Reserva'})

@login_required
def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.user != reserva.usuario and request.user.rol != Usuario.Rol.ADMIN:
        return redirect('mis_reservas')
    
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva actualizada.')
            return redirect('mis_reservas')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'reservas/form.html', {'form': form, 'titulo': 'Editar Reserva'})

@login_required
def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.user != reserva.usuario and request.user.rol != Usuario.Rol.ADMIN:
        return redirect('mis_reservas')
    
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva cancelada.')
        return redirect('mis_reservas')
    return render(request, 'reservas/eliminar.html', {'reserva': reserva})

@login_required
def reporte_sql(request):
    if request.user.rol != Usuario.Rol.ADMIN:
        return redirect('home')
    
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT u.username, m.numero_mesa, r.fecha_reserva, r.hora_inicio 
            FROM reservas_reserva r
            JOIN usuarios_usuario u ON r.usuario_id = u.id
            JOIN mesas_mesa m ON r.mesa_id = m.id
            ORDER BY r.fecha_reserva DESC
        ''')
        rows = cursor.fetchall()
    
    return render(request, 'reservas/reporte_sql.html', {'rows': rows})
