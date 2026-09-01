from django.urls import path
from . import views

urlpatterns = [
    # Ruta principal que muestra los productos
    path('', views.listado_productos, name='listado_productos'),
    path('vender/', views.registrar_venta, name='registrar_venta'),
]