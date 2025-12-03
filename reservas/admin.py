from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mesa', 'fecha_reserva', 'hora_inicio', 'hora_fin', 'created_at')
    list_filter = ('fecha_reserva', 'mesa')
    search_fields = ('usuario__username', 'mesa__numero_mesa')
    date_hierarchy = 'fecha_reserva'
    readonly_fields = ('created_at',)
