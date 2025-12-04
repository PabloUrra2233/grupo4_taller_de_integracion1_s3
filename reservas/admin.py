from django.contrib import admin
from .models import BloqueHorario, DisponibilidadSala, Reserva


@admin.register(BloqueHorario)
class BloqueHorarioAdmin(admin.ModelAdmin):
    list_display = ("hora_inicio", "hora_fin")


@admin.register(DisponibilidadSala)
class DisponibilidadSalaAdmin(admin.ModelAdmin):
    list_display = ("sala", "dia_semana", "bloque", "activa")
    list_filter = ("sala", "dia_semana", "activa")


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("mesa", "fecha_reserva", "bloque", "usuario", "estado")
    list_filter = ("fecha_reserva", "mesa__sala", "estado")
    search_fields = ("usuario__email", "mesa__sala__nombre")
