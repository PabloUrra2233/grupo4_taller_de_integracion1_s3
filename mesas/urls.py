from django.urls import path
from . import views

urlpatterns = [
    path('mesas/', views.lista_mesas, name='lista_mesas'),
    path('mesas/crear/', views.crear_mesa, name='crear_mesa'),
    path('mesas/<int:pk>/editar/', views.editar_mesa, name='editar_mesa'),
    path('mesas/<int:pk>/eliminar/', views.eliminar_mesa, name='eliminar_mesa'),
]
