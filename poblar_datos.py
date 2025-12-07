# -*- coding: utf-8 -*-
"""
Script para poblar la base de datos con datos de prueba
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reserva_mesas.settings')
django.setup()

from usuarios.models import Usuario
from mesas.models import Mesa
from reservas.models import Reserva
from django.utils import timezone

print("Poblando base de datos...")

# 1. Crear superusuario admin
print("\n1. Creando superusuario admin...")
if not Usuario.objects.filter(email='admin@admin.com').exists():
    admin = Usuario.objects.create_superuser(
        username='admin@admin.com',
        email='admin@admin.com',
        password='admin123',
        first_name='Admin',
        last_name='Sistema',
        rol=Usuario.Rol.ADMIN
    )
    print(f"   OK Superusuario creado: {admin.email} / admin123")
else:
    admin = Usuario.objects.get(email='admin@admin.com')
    print(f"   INFO Superusuario ya existe: {admin.email}")

# 2. Crear usuarios meseros
print("\n2. Creando usuarios meseros...")
meseros_data = [
    {'email': 'mesero1@resto.com', 'first_name': 'Carlos', 'last_name': 'Gonzalez'},
    {'email': 'mesero2@resto.com', 'first_name': 'Maria', 'last_name': 'Rodriguez'},
    {'email': 'mesero3@resto.com', 'first_name': 'Pedro', 'last_name': 'Martinez'},
]

meseros = []
for data in meseros_data:
    if not Usuario.objects.filter(email=data['email']).exists():
        mesero = Usuario.objects.create_user(
            username=data['email'],
            email=data['email'],
            password='mesero123',
            first_name=data['first_name'],
            last_name=data['last_name'],
            rol=Usuario.Rol.MESERO
        )
        meseros.append(mesero)
        print(f"   OK Mesero creado: {mesero.email} / mesero123")
    else:
        mesero = Usuario.objects.get(email=data['email'])
        meseros.append(mesero)
        print(f"   INFO Mesero ya existe: {mesero.email}")

# 3. Crear usuarios clientes
print("\n3. Creando usuarios clientes...")
clientes_data = [
    {'email': 'cliente1@email.com', 'first_name': 'Ana', 'last_name': 'Lopez'},
    {'email': 'cliente2@email.com', 'first_name': 'Luis', 'last_name': 'Fernandez'},
    {'email': 'cliente3@email.com', 'first_name': 'Sofia', 'last_name': 'Torres'},
    {'email': 'cliente4@email.com', 'first_name': 'Diego', 'last_name': 'Ramirez'},
]

clientes = []
for data in clientes_data:
    if not Usuario.objects.filter(email=data['email']).exists():
        cliente = Usuario.objects.create_user(
            username=data['email'],
            email=data['email'],
            password='cliente123',
            first_name=data['first_name'],
            last_name=data['last_name'],
            rol=Usuario.Rol.CLIENTE
        )
        clientes.append(cliente)
        print(f"   OK Cliente creado: {cliente.email} / cliente123")
    else:
        cliente = Usuario.objects.get(email=data['email'])
        clientes.append(cliente)
        print(f"   INFO Cliente ya existe: {cliente.email}")

# 4. Crear mesas
print("\n4. Creando mesas...")
mesas_data = [
    {'numero': 1, 'capacidad': 2, 'disponible': True},
    {'numero': 2, 'capacidad': 4, 'disponible': True},
    {'numero': 3, 'capacidad': 4, 'disponible': True},
    {'numero': 4, 'capacidad': 6, 'disponible': True},
    {'numero': 5, 'capacidad': 6, 'disponible': True},
    {'numero': 6, 'capacidad': 8, 'disponible': True},
    {'numero': 7, 'capacidad': 2, 'disponible': True},
    {'numero': 8, 'capacidad': 4, 'disponible': True},
    {'numero': 9, 'capacidad': 10, 'disponible': False},
    {'numero': 10, 'capacidad': 8, 'disponible': True},
]

mesas = []
for data in mesas_data:
    mesa, created = Mesa.objects.get_or_create(
        numero=data['numero'],
        defaults={'capacidad': data['capacidad'], 'disponible': data['disponible']}
    )
    mesas.append(mesa)
    if created:
        print(f"   OK Mesa {mesa.numero} creada - Capacidad: {mesa.capacidad} personas")
    else:
        print(f"   INFO Mesa {mesa.numero} ya existe")

# 5. Crear reservas
print("\n5. Creando reservas de prueba...")
hoy = timezone.now()
reservas_data = [
    # Reservas pasadas
    {'cliente': clientes[0], 'mesa': mesas[0], 'dias': -2, 'hora': 19, 'estado': 'COMPLETADA'},
    {'cliente': clientes[1], 'mesa': mesas[1], 'dias': -1, 'hora': 20, 'estado': 'COMPLETADA'},
    
    # Reservas de hoy
    {'cliente': clientes[2], 'mesa': mesas[2], 'dias': 0, 'hora': 18, 'estado': 'CONFIRMADA'},
    {'cliente': clientes[3], 'mesa': mesas[3], 'dias': 0, 'hora': 21, 'estado': 'CONFIRMADA'},
    
    # Reservas futuras
    {'cliente': clientes[0], 'mesa': mesas[4], 'dias': 1, 'hora': 19, 'estado': 'PENDIENTE'},
    {'cliente': clientes[1], 'mesa': mesas[5], 'dias': 2, 'hora': 20, 'estado': 'PENDIENTE'},
    {'cliente': clientes[2], 'mesa': mesas[6], 'dias': 3, 'hora': 19, 'estado': 'CONFIRMADA'},
    {'cliente': clientes[3], 'mesa': mesas[7], 'dias': 5, 'hora': 21, 'estado': 'PENDIENTE'},
    
    # Reserva cancelada
    {'cliente': clientes[0], 'mesa': mesas[1], 'dias': 7, 'hora': 18, 'estado': 'CANCELADA'},
]

for i, data in enumerate(reservas_data):
    fecha = (hoy + timedelta(days=data['dias'])).date()
    hora = timezone.datetime.combine(fecha, timezone.datetime.min.time()).replace(hour=data['hora'])
    
    if not Reserva.objects.filter(cliente=data['cliente'], fecha_hora=hora, mesa=data['mesa']).exists():
        reserva = Reserva.objects.create(
            cliente=data['cliente'],
            mesa=data['mesa'],
            fecha_hora=hora,
            numero_personas=data['mesa'].capacidad,
            estado=data['estado']
        )
        print(f"   OK Reserva: {data['cliente'].first_name} - Mesa {data['mesa'].numero} - {fecha} {data['hora']}:00 - {data['estado']}")
    else:
        print(f"   INFO Reserva ya existe para {data['cliente'].first_name}")

print("\n" + "="*70)
print("BASE DE DATOS POBLADA EXITOSAMENTE")
print("="*70)

print("\nCREDENCIALES DE ACCESO:")
print("\nSUPERUSUARIO ADMIN:")
print("   Email: admin@admin.com")
print("   Password: admin123")
print("   URL Admin: http://localhost:8000/admin/")

print("\nMESEROS:")
for mesero in meseros_data:
    print(f"   Email: {mesero['email']} / Password: mesero123")

print("\nCLIENTES:")
for cliente in clientes_data:
    print(f"   Email: {cliente['email']} / Password: cliente123")

print("\nMESAS CREADAS: 10 mesas (capacidad de 2 a 10 personas)")
print("RESERVAS CREADAS: 9 reservas (pasadas, hoy y futuras)")

print("\n" + "="*70)
print("Listo para usar!")
print("="*70)
