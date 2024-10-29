from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
import controllers.controlador_resenas as controlador_resenas

# Crear el Blueprint para reseñas
resena_bp = Blueprint('resena_bp', __name__)

# Rutas para la gestión de reseñas en vistas HTML
@resena_bp.route('/menu_man_resena', methods=["GET"])
def menu_man_resena():
    resenas = controlador_resenas.obtener_todas_resenas()
    usuarios = controlador_resenas.obtener_todos_usuarios()
    return render_template('menuManResena.html', resenas=resenas, usuarios=usuarios)

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

@resena_bp.route('/actualizar_resena', methods=["POST"])
def actualizar_resena():
    idResena = request.form.get('idResena')
    descripcion = request.form.get('descripcion')
    idUsuario = request.form.get('idUsuario')
    
    if not idResena or not descripcion or not idUsuario:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('resena_bp.menu_man_resena'))

    try:
        controlador_resenas.actualizar_resena(idResena, descripcion, idUsuario)
        flash("Reseña actualizada exitosamente", "success")
    except Exception as e:
        flash(f"Error al actualizar reseña: {str(e)}", "error")

    return redirect(url_for('resena_bp.menu_man_resena'))

@resena_bp.route('/eliminar_resena/<int:idResena>', methods=["POST"])
def eliminar_resena(idResena):
    try:
        controlador_resenas.eliminar_resena(idResena)
        flash("Reseña eliminada exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar reseña: {str(e)}", "error")
    
    return redirect(url_for('resena_bp.menu_man_resena'))


# Rutas de API para la gestión de reseñas
# API para agregar una reseña desde JSON
@resena_bp.route("/api/agregar_resena", methods=["POST"])
def agregar_resena_api():
    try:
        descripcion = request.json["descripcion"]
        idUsuario = request.json["idUsuario"]
        controlador_resenas.agregar_resena(descripcion, idUsuario)
        return jsonify({"data": [], "message": "Reseña agregada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para actualizar una reseña
@resena_bp.route("/api/actualizar_resena", methods=["POST"])
def actualizar_resena_api():
    try:
        idResena = request.json["idResena"]
        descripcion = request.json["descripcion"]
        idUsuario = request.json["idUsuario"]
        controlador_resenas.actualizar_resena(idResena, descripcion, idUsuario)
        return jsonify({"message": "Reseña actualizada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para eliminar una reseña
@resena_bp.route("/api/eliminar_resena/<int:idResena>", methods=["POST"])
def eliminar_resena_api(idResena):
    try:
        controlador_resenas.eliminar_resena(idResena)
        return jsonify({"message": "Reseña eliminada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(e), "status": -1})

# API para listar todas las reseñas
@resena_bp.route("/api/listar_resenas", methods=["GET"])
def listar_resenas_api():
    try:
        resenas = controlador_resenas.obtener_todas_resenas()
        return jsonify({"data": resenas, "message": "Reseñas obtenidas correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para listar reseñas de un usuario por ID
@resena_bp.route("/api/listar_resenas_usuario/<int:idUsuario>", methods=["GET"])
def listar_resenas_usuario_api(idUsuario):
    try:
        resenas_usuario = controlador_resenas.obtener_resenas_por_usuario(idUsuario)
        return jsonify({"data": resenas_usuario, "message": "Reseñas del usuario obtenidas correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})
