from flask import Blueprint, render_template, request, redirect, url_for, flash
import controllers.controlador_resenas as controlador_resenas

# Crear el Blueprint para reseñas
resena_bp = Blueprint('resena_bp', __name__)

# Ruta para mostrar la página de gestión de reseñas
@resena_bp.route('/menu_man_resena', methods=["GET"])
def menu_man_resena():
    resenas = controlador_resenas.obtener_todas_resenas()
    usuarios = controlador_resenas.obtener_todos_usuarios()
    return render_template('menuManResena.html', resenas=resenas, usuarios=usuarios)

# Ruta para agregar una nueva reseña
@resena_bp.route('/agregar_resena', methods=["POST"])
def agregar_resena():
    descripcion = request.form.get('descripcion')
    idUsuario = request.form.get('idUsuario')
    
    if not descripcion or not idUsuario:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('resena_bp.menu_man_resena'))

    try:
        controlador_resenas.agregar_resena(descripcion, idUsuario)
        flash("Reseña agregada exitosamente", "success")
    except Exception as e:
        flash(f"Error al agregar reseña: {str(e)}", "error")
    
    return redirect(url_for('resena_bp.menu_man_resena'))

# Ruta para actualizar una reseña
@resena_bp.route('/actualizar_resena', methods=["POST"])
def actualizar_resena():
    idResena = request.form.get('idResena')  # Asegúrate de recibir este ID
    descripcion = request.form.get('descripcion')
    idUsuario = request.form.get('idUsuario')  # Asegúrate de recibir el idUsuario
    
    if not idResena or not descripcion or not idUsuario:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('resena_bp.menu_man_resena'))

    try:
        controlador_resenas.actualizar_resena(idResena, descripcion, idUsuario)  # Llamar con los tres parámetros
        flash("Reseña actualizada exitosamente", "success")
    except Exception as e:
        flash(f"Error al actualizar reseña: {str(e)}", "error")

    return redirect(url_for('resena_bp.menu_man_resena'))

# Ruta para eliminar una reseña
@resena_bp.route('/eliminar_resena/<int:idResena>', methods=["POST"])
def eliminar_resena(idResena):
    try:
        controlador_resenas.eliminar_resena(idResena)
        flash("Reseña eliminada exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar reseña: {str(e)}", "error")
    
    return redirect(url_for('resena_bp.menu_man_resena'))
