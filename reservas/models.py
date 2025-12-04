from django.conf import settings
from django.db import models
from mesas.models import Mesa, Sala


class BloqueHorario(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        ordering = ["hora_inicio"]

    def __str__(self):
        return f"{self.hora_inicio.strftime('%H:%M')} – {self.hora_fin.strftime('%H:%M')}"


class DisponibilidadSala(models.Model):
    """
    Define en qué días y bloques una sala está disponible.
    dia_semana: 0=Lunes ... 6=Domingo
    """
    DIA_SEMANA_CHOICES = [
        (0, "Lunes"),
        (1, "Martes"),
        (2, "Miércoles"),
        (3, "Jueves"),
        (4, "Viernes"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="disponibilidades")
    bloque = models.ForeignKey(BloqueHorario, on_delete=models.CASCADE, related_name="disponibilidades")
    dia_semana = models.IntegerField(choices=DIA_SEMANA_CHOICES)
    activa = models.BooleanField(default=True)

    class Meta:
        unique_together = ("sala", "bloque", "dia_semana")
        ordering = ["sala__nombre", "dia_semana", "bloque__hora_inicio"]

    def __str__(self):
        return f"{self.sala} – {self.get_dia_semana_display()} – {self.bloque}"


class EstadoReserva(models.TextChoices):
    PENDIENTE = "pendiente", "Pendiente"
    CONFIRMADA = "confirmada", "Confirmada"
    CANCELADA = "cancelada", "Cancelada"


class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name="reservas")
    fecha_reserva = models.DateField()
    bloque = models.ForeignKey(BloqueHorario, on_delete=models.CASCADE, related_name="reservas")
    estado = models.CharField(
        max_length=20,
        choices=EstadoReserva.choices,
        default=EstadoReserva.PENDIENTE,
    )
    comentario = models.TextField(blank=True, null=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("mesa", "fecha_reserva", "bloque")
        ordering = ["-fecha_reserva", "bloque__hora_inicio"]

    def __str__(self):
        return f"{self.mesa} – {self.fecha_reserva} – {self.bloque}"
