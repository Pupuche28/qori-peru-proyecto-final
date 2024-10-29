from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
import controllers.controlador_roles as controlador_roles  # Importa el controlador de roles

# Crear el Blueprint para roles
rol_bp = Blueprint('rol_bp', __name__)

# Rutas para la gestión de roles en vistas HTML
@rol_bp.route('/menu_man_rol', methods=["GET"])
def menu_man_rol():
    roles = controlador_roles.obtener_roles()  # Llama al controlador para obtener roles
    return render_template('menuManRol.html', roles=roles)

@rol_bp.route('/agregar_rol', methods=["POST"])
def agregar_rol():
    nombre = request.form.get('nombre')
    if not nombre:
        flash("El nombre del rol es obligatorio", "error")
        return redirect(url_for('rol_bp.menu_man_rol'))

    controlador_roles.agregar_rol(nombre)  # Llama al controlador para agregar el rol
    flash("Rol agregado exitosamente", "success")
    return redirect(url_for('rol_bp.menu_man_rol'))

@rol_bp.route('/actualizar_rol', methods=["POST"])
def actualizar_rol():
    idRol = request.form.get('idRol')
    nombre = request.form.get('nombre')
    if not idRol or not nombre:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('rol_bp.menu_man_rol'))

    controlador_roles.actualizar_rol(idRol, nombre)  # Llama al controlador para actualizar el rol
    flash("Rol actualizado exitosamente", "success")
    return redirect(url_for('rol_bp.menu_man_rol'))

@rol_bp.route('/eliminar_rol/<int:idRol>', methods=["POST"])
def eliminar_rol(idRol):
    controlador_roles.eliminar_rol(idRol)  # Llama al controlador para eliminar el rol
    flash("Rol eliminado exitosamente", "success")
    return redirect(url_for('rol_bp.menu_man_rol'))


# Rutas de API para la gestión de roles
# API para agregar un rol desde JSON
@rol_bp.route("/api/agregar_rol", methods=["POST"])
def agregar_rol_api():
    try:
        nombre = request.json["nombre"]
        controlador_roles.agregar_rol(nombre)
        return jsonify({"data": [], "message": "Rol agregado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para actualizar un rol
@rol_bp.route("/api/actualizar_rol", methods=["POST"])
def actualizar_rol_api():
    try:
        idRol = request.json["idRol"]
        nombre = request.json["nombre"]
        controlador_roles.actualizar_rol(idRol, nombre)
        return jsonify({"message": "Rol actualizado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para eliminar un rol
@rol_bp.route("/api/eliminar_rol/<int:idRol>", methods=["POST"])
def eliminar_rol_api(idRol):
    try:
        controlador_roles.eliminar_rol(idRol)
        return jsonify({"message": "Rol eliminado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(e), "status": -1})

# API para listar todos los roles
@rol_bp.route("/api/listar_roles", methods=["GET"])
def listar_roles_api():
    try:
        roles = controlador_roles.obtener_roles()
        return jsonify({"data": roles, "message": "Roles obtenidos correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})
