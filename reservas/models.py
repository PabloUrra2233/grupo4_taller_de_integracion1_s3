from django.db import models
from django.conf import settings
from mesas.models import Mesa
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    comentario = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.usuario} para Mesa {self.mesa.numero_mesa} el {self.fecha_reserva}"

    # VALIDACIÓN AQUÍ DENTRO
    def clean(self):
        hoy = timezone.localdate()
        max_dias = hoy + timedelta(days=7)

        # --- Validación de rango de fechas ---
        if self.fecha_reserva < hoy:
            raise ValidationError("No puedes reservar en una fecha pasada.")

        if self.fecha_reserva > max_dias:
            raise ValidationError("Solo puedes reservar dentro de los próximos 7 días.")

        # --- No permitir sábados ni domingos ---
        # weekday(): lunes=0 ... domingo=6
        if self.fecha_reserva.weekday() in [5, 6]:
            raise ValidationError("No se puede reservar sábado ni domingo.")

        # --- Validación de horario ---
        # Hora mínima permitida: 08:00
        # Hora máxima permitida: 19:00 (19:00 es la hora en que debe terminar la reserva)
        from datetime import time
        hora_min = time(8, 0)
        hora_max = time(19, 0)

        if not (hora_min <= self.hora_inicio <= hora_max):
            raise ValidationError("La hora de inicio debe ser entre las 08:00 y 19:00.")

        if not (hora_min <= self.hora_fin <= hora_max):
            raise ValidationError("La hora de término debe ser entre las 08:00 y 19:00.")

        # Asegurar que la hora de fin sea mayor que la de inicio
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de término debe ser mayor que la hora de inicio.")

