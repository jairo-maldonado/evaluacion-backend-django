from django.db import models

# Modelo para gestionar clientes según el requerimiento de cliente habitual o casual
class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT del Cliente")
    es_habitual = models.BooleanField(default=False, verbose_name="¿Es cliente habitual?")
    nombre = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre Completo")

    def __str__(self):
        return f"{self.rut} - {'Habitual' if self.es_habitual else 'Solo Boleta'}"

# Modelo para registrar el producto con nombre, código, cantidad y precio
class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código del Producto")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    precio = models.IntegerField(verbose_name="Precio de Venta")
    stock = models.IntegerField(verbose_name="Cantidad en Stock")

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock})"

# Modelo para vincular la venta de un producto a un cliente específico
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_vendida = models.IntegerField(verbose_name="Cantidad")
    fecha_venta = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    def __str__(self):
        return f"Venta de {self.cantidad_vendida}x {self.producto.nombre} a {self.cliente.rut}"
