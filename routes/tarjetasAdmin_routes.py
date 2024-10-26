from flask import Blueprint, render_template, request, redirect, url_for, flash
import controllers.controlador_tarjetasAdmin as controlador_tarjetas

# Crear el Blueprint para tarjetas bajo la nueva denominación tarjetaAdmin_bp
tarjetaAdmin_bp = Blueprint('tarjetaAdmin_bp', __name__)

# Ruta para mostrar la página de gestión de tarjetas
@tarjetaAdmin_bp.route('/menu_man_tarjeta', methods=["GET"])
def menu_man_tarjeta():
    tarjetas = controlador_tarjetas.obtener_todas_tarjetas()
    usuarios = controlador_tarjetas.obtener_todos_usuarios()
    return render_template('menuManTarjeta.html', tarjetas=tarjetas, usuarios=usuarios)

# Ruta para agregar una nueva tarjeta
@tarjetaAdmin_bp.route('/agregar_tarjeta', methods=["POST"])
def agregar_tarjeta():
    nombre = request.form.get('nombre')
    nroTarjeta = request.form.get('nroTarjeta')
    fecha = request.form.get('fecha')
    idUsuario = request.form.get('idUsuario')
    
    controlador_tarjetas.agregar_tarjeta(nombre, nroTarjeta, fecha, idUsuario)
    flash("Tarjeta agregada exitosamente", "success")
    return redirect(url_for('tarjetaAdmin_bp.menu_man_tarjeta'))

# Ruta para actualizar una tarjeta
@tarjetaAdmin_bp.route('/actualizar_tarjeta', methods=["POST"])
def actualizar_tarjeta():
    idTarjeta = request.form.get('idTarjeta')
    nombre = request.form.get('nombre')
    nroTarjeta = request.form.get('nroTarjeta')
    fecha = request.form.get('fecha')
    idUsuario = request.form.get('idUsuario')
    
    controlador_tarjetas.actualizar_tarjeta(idTarjeta, nombre, nroTarjeta, fecha, idUsuario)
    flash("Tarjeta actualizada exitosamente", "success")
    return redirect(url_for('tarjetaAdmin_bp.menu_man_tarjeta'))

# Ruta para eliminar una tarjeta
@tarjetaAdmin_bp.route('/eliminar_tarjeta/<int:idTarjeta>', methods=["POST"])
def eliminar_tarjeta(idTarjeta):
    controlador_tarjetas.eliminar_tarjeta(idTarjeta)
    flash("Tarjeta eliminada exitosamente", "success")
    return redirect(url_for('tarjetaAdmin_bp.menu_man_tarjeta'))
