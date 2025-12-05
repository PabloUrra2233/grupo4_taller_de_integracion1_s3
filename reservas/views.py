from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib import messages
from .models import Reserva
from .forms import ReservaForm
from usuarios.models import Usuario
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.http import JsonResponse

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

            # --- Regla 1: Máximo 1 reserva por día ---
            existe_misma_fecha = Reserva.objects.filter(
                usuario=request.user,
                fecha_reserva=reserva.fecha_reserva
            ).exists()

            if existe_misma_fecha:
                messages.error(request, 'Ya tienes una reserva para este día.')
                return render(request, 'reservas/form.html', {'form': form, 'titulo': 'Nueva Reserva'})
            
            # --- Regla 2: Máximo 3 reservas por semana ---
            anio, semana, _ = reserva.fecha_reserva.isocalendar()

            reservas_semana = Reserva.objects.filter(
                usuario=request.user,
                fecha_reserva__year=anio,
                fecha_reserva__week=semana,
            ).count()

            if reservas_semana >= 3:
                messages.error(request, 'Has alcanzado el límite de 3 reservas esta semana.')
                return render(request, 'reservas/form.html', {'form': form, 'titulo': 'Nueva Reserva'})

            # --- Validaciones del modelo (clean) ---
            try:
                reserva.save()  # aquí se ejecuta clean()
            except ValidationError as e:
                form.add_error(None, e.message)  # muestra el mensaje en el formulario
                return render(request, 'reservas/form.html', {'form': form, 'titulo': 'Nueva Reserva'})

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



@login_required
def obtener_horarios_ocupados(request):
    mesa_id = request.GET.get('mesa_id')
    fecha = request.GET.get('fecha')

    reservas = Reserva.objects.filter(
        mesa_id=mesa_id,
        fecha_reserva=fecha
    ).values('hora_inicio', 'hora_fin')

    return JsonResponse(list(reservas), safe=False)
