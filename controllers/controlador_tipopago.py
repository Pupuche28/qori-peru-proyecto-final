from bd import obtener_conexion
from datetime import datetime
from decimal import Decimal

# Función para crear un nuevo pedido
def crear_pedido(conexion, id_usuario):
    """
    Insertar un nuevo pedido en la tabla PEDIDO y devolver el ID del pedido.
    """
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO PEDIDO (fechainicio, estado, idUsuario)
            VALUES (%s, %s, %s)
        """, (datetime.now(), 'Pendiente de Entrega', id_usuario))
        
        # Obtener el ID del pedido recién creado
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_pedido = cursor.fetchone()[0]
    
    return id_pedido

# Función para registrar el pago
def registrar_pago(conexion, id_pedido, monto, id_tarjeta):
    """
    Insertar el registro de pago en la tabla PAGO.
    """
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO PAGO (fechapago, monto, metodopago, idPedido, idTarjeta)
            VALUES (%s, %s, %s, %s, %s)
        """, (datetime.now(), monto, 'Tarjeta de Débito', id_pedido, id_tarjeta))

# Función para registrar los detalles del pedido
def registrar_detalle_pedido(conexion, id_pedido, carrito):
    """
    Insertar los detalles del pedido en la tabla DETALLE_PEDIDO para cada producto en el carrito.
    """
    with conexion.cursor() as cursor:
        for item in carrito:
            nombre_producto = item['name']  # Usar el nombre del producto para obtener los detalles desde la base de datos
            cantidad = item['quantity']  # La cantidad de productos que el usuario está comprando

            # Buscar el producto en la base de datos para obtener su precio, descuento y stock actual
            cursor.execute("SELECT idProducto, precio, descuento, stock FROM PRODUCTO WHERE nombredeproducto = %s", (nombre_producto,))
            result = cursor.fetchone()
            if result:
                id_producto = result[0]
                precio = Decimal(result[1])  # Convertir el precio a Decimal
                descuento = Decimal(result[2])  # Convertir el descuento a Decimal
                stock_actual = result[3]  # Obtener el stock actual del producto
                print(f"Producto encontrado: {nombre_producto}, Precio: {precio}, Descuento: {descuento}, Stock: {stock_actual}")
            else:
                raise Exception(f"No se encontró el producto con nombre: {nombre_producto}")

            # Verificar si hay suficiente stock
            if cantidad > stock_actual:
                raise Exception(f"No hay suficiente stock disponible para {nombre_producto}")

            # Calcular el IGV sobre el precio (que ya tiene el descuento aplicado)
            igv = calcular_igv(precio * cantidad)

            # Subtotal: el precio total del producto sin IGV
            subtotal = precio * cantidad

            # Total: igual que el subtotal, sin sumar el IGV
            total = subtotal

            # Insertar el detalle del pedido con el precio, descuento, IGV, subtotal y total
            cursor.execute("""
                INSERT INTO DETALLE_PEDIDO (idPedido, idProducto, cantidad, precio, descuento, igv, subtotal, total)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_pedido, id_producto, cantidad, precio, descuento, igv, subtotal, total))

            # Actualizar el stock del producto restando la cantidad comprada
            nuevo_stock = stock_actual - cantidad
            cursor.execute("""
                UPDATE PRODUCTO
                SET stock = %s
                WHERE idProducto = %s
            """, (nuevo_stock, id_producto))

            print(f"Stock actualizado para {nombre_producto}: {nuevo_stock} unidades restantes.")

# Función para calcular el IGV
def calcular_igv(subtotal, porcentaje=Decimal('0.18')):
    """
    Calcular el IGV basado en un porcentaje fijo (18%).
    """
    return subtotal * porcentaje  # Usamos Decimal para asegurar la precisión
