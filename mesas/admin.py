from django.contrib import admin
from .models import Mesa
from reservas.models import Reserva

class ReservaInline(admin.TabularInline):
    model = Reserva
    extra = 0
    readonly_fields = ('usuario', 'fecha_reserva', 'hora_inicio', 'hora_fin')
    can_delete = False

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero_mesa', 'capacidad', 'ubicacion', 'estado')
    list_filter = ('estado', 'capacidad')
    search_fields = ('ubicacion',)
    inlines = [ReservaInline]
