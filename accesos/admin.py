from django.contrib import admin
from .models import LogAcceso

@admin.register(LogAcceso)
class LogAccesoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha_hora')
    list_filter = ('accion', 'fecha_hora')
    search_fields = ('usuario__username',)
    readonly_fields = ('usuario', 'accion', 'fecha_hora')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
