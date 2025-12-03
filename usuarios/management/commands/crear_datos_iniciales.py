from django.core.management.base import BaseCommand
from usuarios.models import Usuario
from mesas.models import Mesa

class Command(BaseCommand):
    help = 'Crea datos iniciales para la aplicación'

    def handle(self, *args, **kwargs):
        # Crear superusuario admin
        if not Usuario.objects.filter(username='admin').exists():
            admin = Usuario.objects.create_superuser(
                username='admin',
                email='admin@universidad.cl',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                rol=Usuario.Rol.ADMIN
            )
            self.stdout.write(self.style.SUCCESS(f'Admin creado: {admin.username}'))

        # Crear segundo admin
        if not Usuario.objects.filter(email='admin2@universidad.cl').exists():
            admin2 = Usuario.objects.create_user(
                username='admin2@universidad.cl',
                email='admin2@universidad.cl',
                password='admin123',
                first_name='María',
                last_name='González',
                rol=Usuario.Rol.ADMIN,
                is_staff=True
            )
            self.stdout.write(self.style.SUCCESS(f'Admin 2 creado: {admin2.username}'))


        # Crear usuarios de prueba
        usuarios_test = [
            {'username': 'juan@alumno.cl', 'email': 'juan@alumno.cl', 'password': 'test123', 
             'first_name': 'Juan', 'last_name': 'Pérez', 'rol': Usuario.Rol.ALUMNO},
            {'username': 'maria@alumno.cl', 'email': 'maria@alumno.cl', 'password': 'test123', 
             'first_name': 'María', 'last_name': 'López', 'rol': Usuario.Rol.ALUMNO},
            {'username': 'carlos@funcionario.cl', 'email': 'carlos@funcionario.cl', 'password': 'test123', 
             'first_name': 'Carlos', 'last_name': 'Rodríguez', 'rol': Usuario.Rol.FUNCIONARIO},
        ]

        for user_data in usuarios_test:
            if not Usuario.objects.filter(email=user_data['email']).exists():
                Usuario.objects.create_user(**user_data)
                self.stdout.write(self.style.SUCCESS(f'Usuario creado: {user_data["email"]}'))

        # Crear 10 mesas
        mesas_data = [
            {'numero_mesa': 1, 'capacidad': 4, 'ubicacion': 'Biblioteca - Sala A'},
            {'numero_mesa': 2, 'capacidad': 6, 'ubicacion': 'Biblioteca - Sala A'},
            {'numero_mesa': 3, 'capacidad': 2, 'ubicacion': 'Biblioteca - Sala B'},
            {'numero_mesa': 4, 'capacidad': 4, 'ubicacion': 'Biblioteca - Sala B'},
            {'numero_mesa': 5, 'capacidad': 8, 'ubicacion': 'Cafetería'},
            {'numero_mesa': 6, 'capacidad': 4, 'ubicacion': 'Cafetería'},
            {'numero_mesa': 7, 'capacidad': 6, 'ubicacion': 'Sala de Estudio 1'},
            {'numero_mesa': 8, 'capacidad': 4, 'ubicacion': 'Sala de Estudio 1'},
            {'numero_mesa': 9, 'capacidad': 10, 'ubicacion': 'Sala de Conferencias'},
            {'numero_mesa': 10, 'capacidad': 2, 'ubicacion': 'Terraza'},
        ]

        for mesa_data in mesas_data:
            if not Mesa.objects.filter(numero_mesa=mesa_data['numero_mesa']).exists():
                Mesa.objects.create(**mesa_data)
                self.stdout.write(self.style.SUCCESS(f'Mesa {mesa_data["numero_mesa"]} creada'))

        self.stdout.write(self.style.SUCCESS('\nDatos iniciales creados exitosamente!'))
        self.stdout.write(self.style.WARNING('\nCredenciales de acceso:'))
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Alumno: juan@alumno.cl / test123')

