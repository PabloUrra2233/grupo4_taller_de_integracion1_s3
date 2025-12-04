from django.db import models


class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Mesa(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="mesas")
    numero_mesa = models.IntegerField()
    capacidad = models.IntegerField(default=1)
    activa = models.BooleanField(default=True)

    class Meta:
        unique_together = ("sala", "numero_mesa")
        ordering = ["sala__nombre", "numero_mesa"]

    def __str__(self):
        return f"{self.sala.nombre} – Mesa {self.numero_mesa}"
