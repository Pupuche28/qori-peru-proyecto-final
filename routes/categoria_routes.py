from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import controllers.controlador_categorias as controlador_categorias  # Importa el controlador de categorías
import controllers.controlador_productos as controlador_productos  # Importa el controlador de productos

# Crear el Blueprint para categorías
categoria_bp = Blueprint('categoria_bp', __name__)

# Ruta para mostrar la página de gestión de categorías
@categoria_bp.route('/menu_man_categoria', methods=["GET"])
def menu_man_categoria():
    categorias = controlador_categorias.obtener_todas_categorias()  # Llama al controlador para obtener categorías
    return render_template('menuManCategoria.html', categorias=categorias)

# Ruta para agregar una nueva categoría
@categoria_bp.route('/agregar_categoria', methods=["POST"])
def agregar_categoria():
    nombre = request.form.get('nombre')
    if not nombre:
        flash("El nombre de la categoría es obligatorio", "error")
        return redirect(url_for('categoria_bp.menu_man_categoria'))

    controlador_categorias.agregar_categoria(nombre)  # Llama al controlador para agregar la categoría
    flash("Categoría agregada exitosamente", "success")
    return redirect(url_for('categoria_bp.menu_man_categoria'))

# Ruta para actualizar una categoría
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

# Ruta para eliminar una categoría desde el administrador
@categoria_bp.route("/eliminar_administrador/<int:idCategoria>", methods=["POST"])
def eliminar_categoria(idCategoria):
    try:
        # Eliminamos la categoría y la BD se encarga de eliminar los productos asociados (CASCADE)
        controlador_categorias.eliminar_categoria(idCategoria)
        flash("Categoría eliminada correctamente junto con sus productos asociados", "success")
    except Exception as e:
        flash(f"Error al eliminar la categoría: {str(e)}", "error")
    return redirect(url_for('categoria_bp.menu_man_categoria'))

# Ruta para verificar si una categoría tiene productos asociados
@categoria_bp.route('/verificar_productos/<int:idCategoria>', methods=['GET'])
def verificar_productos(idCategoria):
    try:
        # Verificamos si la categoría tiene productos asociados
        tiene_productos = controlador_productos.categoria_tiene_productos(idCategoria)
        return jsonify({"tiene_productos": tiene_productos})  # Retorna True o False
    except Exception as e:
        return jsonify({"error": str(e)}), 500
