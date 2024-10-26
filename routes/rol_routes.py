from flask import Blueprint, render_template, request, redirect, url_for, flash
import controllers.controlador_roles as controlador_roles  # Importa el controlador de roles

# Crear el Blueprint para roles
rol_bp = Blueprint('rol_bp', __name__)

# Ruta para mostrar la página de gestión de roles
@rol_bp.route('/menu_man_rol', methods=["GET"])
def menu_man_rol():
    roles = controlador_roles.obtener_roles()  # Llama al controlador para obtener roles
    return render_template('menuManRol.html', roles=roles)

# Ruta para agregar un nuevo rol
@rol_bp.route('/agregar_rol', methods=["POST"])
def agregar_rol():
    nombre = request.form.get('nombre')
    if not nombre:
        flash("El nombre del rol es obligatorio", "error")
        return redirect(url_for('rol_bp.menu_man_rol'))

    controlador_roles.agregar_rol(nombre)  # Llama al controlador para agregar el rol
    flash("Rol agregado exitosamente", "success")
    return redirect(url_for('rol_bp.menu_man_rol'))

# Ruta para actualizar un rol
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

# Ruta para eliminar un rol
@rol_bp.route('/eliminar_rol/<int:idRol>', methods=["POST"])
def eliminar_rol(idRol):
    controlador_roles.eliminar_rol(idRol)  # Llama al controlador para eliminar el rol
    flash("Rol eliminado exitosamente", "success")
    return redirect(url_for('rol_bp.menu_man_rol'))
