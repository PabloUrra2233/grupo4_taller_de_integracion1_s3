from django.db import models

class Mesa(models.Model):
    class Estado(models.TextChoices):
        DISPONIBLE = 'disponible', 'Disponible'
        RESERVADA = 'reservada', 'Reservada'

    numero_mesa = models.IntegerField(unique=True)
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.DISPONIBLE)

    def __str__(self):
        return f"Mesa {self.numero_mesa} - {self.ubicacion} ({self.capacidad} pers.)"
