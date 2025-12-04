from django.contrib import admin
from .models import Sala, Mesa


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ubicacion", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre", "ubicacion")


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ("sala", "numero_mesa", "capacidad", "activa")
    list_filter = ("sala", "activa")
    search_fields = ("sala__nombre",)
