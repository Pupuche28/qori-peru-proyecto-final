from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from controllers.controlador_tarjeta import agregar_tarjeta, obtener_tarjetas

tarjeta_bp = Blueprint('tarjeta_bp', __name__)

# Ruta para mostrar las tarjetas y el formulario (redirige a /tarjetas/tarjetas o /tipopago)
@tarjeta_bp.route('/tarjetas', methods=['GET'])
def tarjetas():
    if not current_user.is_authenticated:
        flash('Por favor, inicia sesión para gestionar tus tarjetas', 'danger')
        return redirect(url_for('autenticacion_bp.login'))

    # Obtener las tarjetas del usuario autenticado
    tarjetas = obtener_tarjetas(current_user.id)
    
    # Renderizar la página de tipo de pago con las tarjetas obtenidas
    return render_template('tipopago.html', tarjetas=tarjetas)

# Ruta para procesar el formulario de agregar tarjeta
@tarjeta_bp.route('/tarjetas/agregar', methods=['POST'])
def agregar_tarjeta_route():
    nombre = request.form.get('nombre')
    nro_tarjeta = request.form.get('nro_tarjeta')
    fecha = request.form.get('fecha')
    ccv = request.form.get('ccv')

    if not nombre or not nro_tarjeta or not fecha or not ccv:
        flash('Todos los campos son obligatorios', 'danger')
        return redirect(url_for('tarjeta_bp.tarjetas'))

    # Usamos 'current_user.id' en lugar de 'idUsuario'
    agregar_tarjeta(nombre, nro_tarjeta, fecha, ccv, current_user.id)
    flash('Tarjeta agregada exitosamente', 'success')
    
    # Redirigir a la ruta de tarjetas o tipo de pago, como prefieras
    return redirect(url_for('tipopago_bp.mostrar_tipo_pago'))
