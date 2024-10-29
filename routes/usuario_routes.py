from flask import Blueprint, jsonify, request, flash, redirect, render_template, url_for
import controllers.controlador_usuarios as controlador_usuarios
import controllers.controlador_resenas as controlador_resenas
import traceback  # Importar traceback para manejo de errores detallado

# Crear el blueprint para usuario
usuario_bp = Blueprint('usuario_bp', __name__)

# Rutas para la gestión de usuarios en vistas HTML
@usuario_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        # Obtener datos del formulario
        nombres = request.form.get("nombres")
        apellidos = request.form.get("apellidos")
        email = request.form.get("email")
        telefono = request.form.get("telefono")
        documento = request.form.get("documento")
        contrasena = request.form.get("contrasena")
        direccion = request.form.get("direccion")

        # Verifica que todos los campos estén presentes
        if not nombres or not apellidos or not email or not telefono or not documento or not contrasena or not direccion:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("usuario_bp.registrar"))

        try:
            # Intentar registrar al usuario en la base de datos
            controlador_usuarios.insertar_usuario(nombres, apellidos, email, telefono, documento, contrasena, direccion, 2)
            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for("home"))  # Redirige a la página de inicio
        except Exception as e:
            print(f"Error al registrar usuario: {str(e)}")
            print(traceback.format_exc())  # Muestra el traceback completo del error
            flash(f"Error al registrar usuario: {str(e)}", "error")
            return redirect(url_for("usuario_bp.registrar"))

    return render_template("registrate.html")

@usuario_bp.route("/menu_administrador", methods=["GET"])
def menu_administrador():
    usuarios = controlador_usuarios.obtener_todos_los_usuarios()
    return render_template("menuAdministrador.html", usuarios=usuarios)

@usuario_bp.route("/menu_man_usuario", methods=["GET"])
def menu_man_usuario():
    usuarios = controlador_usuarios.obtener_todos_los_usuarios()
    return render_template("menuManUsuario.html", usuarios=usuarios)

@usuario_bp.route("/agregar_usuario_administrador", methods=["POST"])
def agregar_usuario_administrador():
    try:
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        documento = request.form["documento"]
        direccion = request.form["direccion"]
        rol = request.form["rol"]

        controlador_usuarios.agregar_usuario(nombres, apellidos, email, telefono, documento, direccion, rol)

        flash("Usuario agregado correctamente", "success")
        return redirect(url_for('usuario_bp.menu_man_usuario'))
    except Exception as e:
        flash(f"Error al agregar usuario: {str(e)}", "error")
        return redirect(url_for('usuario_bp.menu_man_usuario'))

@usuario_bp.route("/actualizar_usuario_administrador", methods=["POST"])
def actualizar_usuario_administrador():
    try:
        idUsuario = request.form["idUsuario"]
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        documento = request.form["documento"]
        direccion = request.form["direccion"]
        rol = request.form["rol"]

        controlador_usuarios.actualizar_usuario_administrador(nombres, apellidos, email, telefono, documento, direccion, rol, idUsuario)
        flash("Usuario actualizado correctamente", "success")
        return redirect(url_for('usuario_bp.menu_man_usuario'))
    except Exception as e:
        flash(f"Error al actualizar usuario: {str(e)}", "error")
        return redirect(url_for('usuario_bp.menu_man_usuario'))

@usuario_bp.route("/eliminar_administrador/<int:idUsuario>", methods=["POST"])
def eliminar_administrador(idUsuario):
    try:
        controlador_usuarios.eliminar_usuario(idUsuario)
        flash("Usuario eliminado correctamente", "success")
        return redirect(url_for('usuario_bp.menu_man_usuario'))
    except Exception as e:
        flash(f"Error al eliminar usuario: {str(e)}", "error")
        return redirect(url_for('usuario_bp.menu_man_usuario'))


# Rutas de API para la gestión de usuarios
# API para registrar usuario desde JSON
@usuario_bp.route("/insertarusuario", methods=["POST"])
def insertar_usuario_desde_json():
    try:
        nombres = request.json["nombres"]
        apellidos = request.json["apellidos"]
        email = request.json["email"]
        telefono = request.json["telefono"]
        nroDocIde = request.json["nroDocIde"]
        contrasena = request.json["contrasena"]
        direccion = request.json["direccion"]
        controlador_usuarios.insertar_usuario(nombres, apellidos, email, telefono, nroDocIde, contrasena, direccion, 2)
        return jsonify({"data": [], "message": "Usuario registrado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para actualizar usuario
@usuario_bp.route("/actualizarusuario", methods=["POST"])
def actualizar_usuario_ruta():
    try:
        idUsuario = request.form["idUsuario"]
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        nroDocIde = request.form["nroDocIde"]
        contrasena = request.form["contrasena"]
        direccion = request.form["direccion"]
        controlador_usuarios.actualizar_usuario(nombres, apellidos, email, telefono, nroDocIde, contrasena, direccion, idUsuario)
        return jsonify({"message": "Usuario actualizado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para eliminar usuario por ID
@usuario_bp.route("/eliminar_administrador/<int:idUsuario>", methods=["POST"])
def eliminar_administrador_api(idUsuario):
    try:
        controlador_usuarios.eliminar_usuario(idUsuario)
        return jsonify({"message": "Usuario eliminado correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(e), "status": -1})

# API para listar todos los usuarios
@usuario_bp.route("/listarusuarios", methods=["GET"])
def listar_usuarios():
    try:
        usuarios = controlador_usuarios.obtener_usuarios()
        return jsonify({"data": usuarios, "message": "Usuarios obtenidos correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para listar un usuario por ID
@usuario_bp.route("/listarusuarios/<int:idUsuario>", methods=["GET"])
def listar_usuario_por_id(idUsuario):
    try:
        usuario = controlador_usuarios.obtener_usuario_por_id(idUsuario)
        if usuario:
            return jsonify({"data": usuario, "message": "Usuario obtenido correctamente", "status": 1})
        else:
            return jsonify({"data": [], "message": "Usuario no encontrado", "status": 0})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para verificar si un usuario tiene reseñas activas
@usuario_bp.route('/verificar_resenas/<int:id_usuario>', methods=['GET'])
def verificar_resenas(id_usuario):
    try:
        tiene_resenas = controlador_resenas.usuario_tiene_resenas(id_usuario)
        return jsonify({"tiene_resenas": tiene_resenas})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
