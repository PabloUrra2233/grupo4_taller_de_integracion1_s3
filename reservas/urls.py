from django.urls import path
from . import views

urlpatterns = [
    path('', views.mis_reservas, name='mis_reservas'),
    path('todas/', views.todas_reservas, name='todas_reservas'),
    path('crear/', views.crear_reserva, name='crear_reserva'),
    path('<int:pk>/editar/', views.editar_reserva, name='editar_reserva'),
    path('<int:pk>/eliminar/', views.eliminar_reserva, name='eliminar_reserva'),
    path('reporte/', views.reporte_sql, name='reporte_sql'),
]
