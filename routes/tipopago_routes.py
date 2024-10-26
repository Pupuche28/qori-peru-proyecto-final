from flask_login import current_user
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
import controllers.controlador_tipopago as controlador_tipopago
from controllers.controlador_tarjeta import obtener_tarjetas
from bd import obtener_conexion

tipopago_bp = Blueprint('tipopago_bp', __name__)

@tipopago_bp.route('/finalizar_compra', methods=["POST"])
def finalizar_compra():
    # Usar current_user para obtener el usuario autenticado con Flask-Login
    if not current_user.is_authenticated:
        return jsonify({"error": "Usuario no autenticado"}), 403

    id_usuario = current_user.id  # ID del usuario autenticado
    data = request.json
    id_tarjeta = data.get('idTarjeta')
    carrito = data.get('carrito')

    if not carrito or len(carrito) == 0:
        return jsonify({"error": "El carrito está vacío"}), 400

    conexion = obtener_conexion()
    try:
        # Iniciar la transacción
        conexion.begin()

        # Crear el pedido
        id_pedido = controlador_tipopago.crear_pedido(conexion, id_usuario)

        # Calcular el monto total del carrito
        total_monto = sum(item['price'] * item['quantity'] for item in carrito)

        # Registrar el pago
        controlador_tipopago.registrar_pago(conexion, id_pedido, total_monto, id_tarjeta)

        # Registrar los detalles del pedido
        controlador_tipopago.registrar_detalle_pedido(conexion, id_pedido, carrito)

        # Confirmar la transacción
        conexion.commit()

        # Retornar respuesta de éxito
        return jsonify({"mensaje": "Compra finalizada exitosamente", "idPedido": id_pedido}), 200
    
    except Exception as e:
        # Revertir transacción en caso de error
        conexion.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        conexion.close()

# Ruta para mostrar la página de tipo de pago con las tarjetas (para /tipopago)
@tipopago_bp.route('/tipopago', methods=["GET"])
def mostrar_tipo_pago():
    return cargar_pagina_tipo_pago()

# Ruta para mostrar la página de tipo de pago con las tarjetas (para /tarjetas/tarjetas)
@tipopago_bp.route('/tarjetas/tarjetas', methods=["GET"])
def mostrar_tarjetas():
    return cargar_pagina_tipo_pago()

# Función reutilizable para cargar la página con las tarjetas
def cargar_pagina_tipo_pago():
    # Verificar si el usuario está autenticado
    if not current_user.is_authenticated:
        flash('Por favor inicia sesión para continuar.', 'error')
        return redirect(url_for('autenticacion_bp.login'))

    # Obtener el idUsuario del usuario autenticado
    id_usuario = current_user.id

    # Obtener las tarjetas del usuario desde la base de datos
    conexion = obtener_conexion()
    tarjetas = obtener_tarjetas(id_usuario)
    conexion.close()

    # Depuración: Verificar que las tarjetas se están obteniendo correctamente
    print(f"Tarjetas obtenidas para el usuario {id_usuario}: {tarjetas}")

    # Renderizar la plantilla de tipo de pago con las tarjetas del usuario
    return render_template('tipopago.html', tarjetas=tarjetas)
