from django.urls import path
from . import views

urlpatterns = [
    path('reservas/', views.mis_reservas, name='mis_reservas'),
    path('reservas/todas/', views.todas_reservas, name='todas_reservas'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/<int:pk>/editar/', views.editar_reserva, name='editar_reserva'),
    path('reservas/<int:pk>/eliminar/', views.eliminar_reserva, name='eliminar_reserva'),
    path('reservas/reporte/', views.reporte_sql, name='reporte_sql'),
]
