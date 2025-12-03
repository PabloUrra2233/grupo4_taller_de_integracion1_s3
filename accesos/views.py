from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import LogAcceso
from usuarios.models import Usuario

def is_admin(user):
    return user.is_authenticated and user.rol == Usuario.Rol.ADMIN

@user_passes_test(is_admin)
def lista_accesos(request):
    logs = LogAcceso.objects.all().select_related('usuario').order_by('-fecha_hora')
    return render(request, 'accesos/lista.html', {'logs': logs})
