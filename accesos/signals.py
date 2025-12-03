from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import LogAcceso

@receiver(user_logged_in)
def log_login(sender, user, request, **kwargs):
    LogAcceso.objects.create(usuario=user, accion=LogAcceso.Accion.LOGIN)

@receiver(user_logged_out)
def log_logout(sender, user, request, **kwargs):
    LogAcceso.objects.create(usuario=user, accion=LogAcceso.Accion.LOGOUT)
