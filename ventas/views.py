from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto, Cliente, Venta

def listado_productos(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/listado.html', {'productos': productos})

def registrar_venta(request):
    if request.method == 'POST':
        rut_cliente = request.POST.get('rut')
        es_habitual = request.POST.get('es_habitual') == 'on'
        nombre_cliente = request.POST.get('nombre', '')
        producto_id = request.POST.get('producto_id')
        
        cantidad = int(request.POST.get('cantidad', 0))
        producto = Producto.objects.get(id=producto_id)

        # VALIDACIÓN: Control de stock y cantidades válidas
        if cantidad <= 0:
            messages.error(request, 'Error: La cantidad debe ser mayor a cero.')
            return redirect('registrar_venta')
        
        elif producto.stock < cantidad:
            messages.error(request, f'Error: Stock insuficiente. Solo quedan {producto.stock} unidades.')
            return redirect('registrar_venta')
        
        else:
            cliente, creado = Cliente.objects.get_or_create(rut=rut_cliente)
            
            if es_habitual:
                cliente.es_habitual = True
                cliente.nombre = nombre_cliente
            cliente.save()

            # OPERACIÓN: Descuento matemático del stock
            producto.stock = producto.stock - cantidad
            producto.save()

            Venta.objects.create(cliente=cliente, producto=producto, cantidad_vendida=cantidad)
            
            messages.success(request, 'Venta registrada con éxito. Stock descontado.')
            return redirect('listado_productos')

    productos_disponibles = Producto.objects.filter(stock__gt=0)
    return render(request, 'ventas/formulario_venta.html', {'productos': productos_disponibles})