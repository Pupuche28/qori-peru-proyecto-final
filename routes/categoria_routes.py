from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
import controllers.controlador_categorias as controlador_categorias  # Importa el controlador de categorías
import controllers.controlador_productos as controlador_productos  # Importa el controlador de productos

# Crear el Blueprint para categorías
categoria_bp = Blueprint('categoria_bp', __name__)

# Rutas para la gestión de categorías en vistas HTML
@categoria_bp.route('/menu_man_categoria', methods=["GET"])
def menu_man_categoria():
    categorias = controlador_categorias.obtener_todas_categorias()  # Llama al controlador para obtener categorías
    return render_template('menuManCategoria.html', categorias=categorias)

@categoria_bp.route('/agregar_categoria', methods=["POST"])
def agregar_categoria():
    nombre = request.form.get('nombre')
    if not nombre:
        flash("El nombre de la categoría es obligatorio", "error")
        return redirect(url_for('categoria_bp.menu_man_categoria'))

    controlador_categorias.agregar_categoria(nombre)  # Llama al controlador para agregar la categoría
    flash("Categoría agregada exitosamente", "success")
    return redirect(url_for('categoria_bp.menu_man_categoria'))

@categoria_bp.route('/actualizar_categoria', methods=["POST"])
def actualizar_categoria():
    idCategoria = request.form.get('idCategoria')
    nombre = request.form.get('nombre')
    if not idCategoria or not nombre:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('categoria_bp.menu_man_categoria'))

    controlador_categorias.actualizar_categoria(idCategoria, nombre)  # Llama al controlador para actualizar la categoría
    flash("Categoría actualizada exitosamente", "success")
    return redirect(url_for('categoria_bp.menu_man_categoria'))

@categoria_bp.route("/eliminar_administrador/<int:idCategoria>", methods=["POST"])
def eliminar_categoria(idCategoria):
    try:
        # Eliminamos la categoría y la BD se encarga de eliminar los productos asociados (CASCADE)
        controlador_categorias.eliminar_categoria(idCategoria)
        flash("Categoría eliminada correctamente junto con sus productos asociados", "success")
    except Exception as e:
        flash(f"Error al eliminar la categoría: {str(e)}", "error")
    return redirect(url_for('categoria_bp.menu_man_categoria'))

@categoria_bp.route('/verificar_productos/<int:idCategoria>', methods=['GET'])
def verificar_productos(idCategoria):
    try:
        # Verificamos si la categoría tiene productos asociados
        tiene_productos = controlador_productos.categoria_tiene_productos(idCategoria)
        return jsonify({"tiene_productos": tiene_productos})  # Retorna True o False
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rutas de API para la gestión de categorías
# API para agregar una categoría desde JSON
@categoria_bp.route("/api/agregar_categoria", methods=["POST"])
def agregar_categoria_api():
    try:
        nombre = request.json["nombre"]
        controlador_categorias.agregar_categoria(nombre)
        return jsonify({"data": [], "message": "Categoría agregada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})

# API para actualizar una categoría
@categoria_bp.route("/api/actualizar_categoria", methods=["POST"])
def actualizar_categoria_api():
    try:
        idCategoria = request.json["idCategoria"]
        nombre = request.json["nombre"]
        controlador_categorias.actualizar_categoria(idCategoria, nombre)
        return jsonify({"message": "Categoría actualizada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(repr(e)), "status": -1})

# API para eliminar una categoría
@categoria_bp.route("/api/eliminar_categoria/<int:idCategoria>", methods=["POST"])
def eliminar_categoria_api(idCategoria):
    try:
        controlador_categorias.eliminar_categoria(idCategoria)
        return jsonify({"message": "Categoría eliminada correctamente", "status": 1})
    except Exception as e:
        return jsonify({"message": str(e), "status": -1})

# API para verificar si una categoría tiene productos asociados
@categoria_bp.route("/api/verificar_productos/<int:idCategoria>", methods=["GET"])
def verificar_productos_api(idCategoria):
    try:
        tiene_productos = controlador_productos.categoria_tiene_productos(idCategoria)
        return jsonify({"tiene_productos": tiene_productos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para listar todas las categorías
@categoria_bp.route("/api/listar_categorias", methods=["GET"])
def listar_categorias_api():
    try:
        categorias = controlador_categorias.obtener_todas_categorias()
        return jsonify({"data": categorias, "message": "Categorías obtenidas correctamente", "status": 1})
    except Exception as e:
        return jsonify({"data": [], "message": str(repr(e)), "status": -1})
