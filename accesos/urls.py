from django.urls import path
from . import views

urlpatterns = [
    path('accesos/', views.lista_accesos, name='lista_accesos'),
]
