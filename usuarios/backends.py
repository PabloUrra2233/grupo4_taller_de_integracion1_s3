from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

Usuario = get_user_model()

class EmailBackend(ModelBackend):
    """
    Backend de autenticación personalizado que permite login con email o username
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Intentar encontrar el usuario por username o email
            user = Usuario.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except Usuario.DoesNotExist:
            # Si no se encuentra el usuario, retornar None
            return None
        except Usuario.MultipleObjectsReturned:
            # Si hay múltiples usuarios, usar el primero encontrado
            user = Usuario.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).first()
        
        # Verificar la contraseña
        if user and user.check_password(password):
            return user
        
        return None
