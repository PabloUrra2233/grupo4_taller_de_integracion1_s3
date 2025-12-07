from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        ALUMNO = 'alumno', 'Alumno'

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ALUMNO)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email', 'rol']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
