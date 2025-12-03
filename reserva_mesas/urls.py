from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('usuarios.urls')),
    path('', include('mesas.urls')),
    path('', include('reservas.urls')),
    path('', include('accesos.urls')),
]
