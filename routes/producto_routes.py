import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import controllers.controlador_productos as controlador_productos

# Crear el Blueprint para productos
producto_bp = Blueprint('producto_bp', __name__)

# Directorio donde se guardarán las imágenes
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'webp'}

# Configurar el directorio de subida de archivos
producto_bp.config = {}
producto_bp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verificar si la carpeta existe, y si no, crearla
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para mostrar la página de gestión de productos
@producto_bp.route('/menu_man_producto', methods=["GET"])
def menu_man_producto():
    productos = controlador_productos.obtener_todos_productos()
    categorias = controlador_productos.obtener_todas_categorias()
    return render_template('menuManProducto.html', productos=productos, categorias=categorias)

# Ruta para agregar un nuevo producto con imagen
@producto_bp.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nombredeproducto = request.form['nombredeproducto']
    autor = request.form.get('autor')
    precio = request.form['precio']
    descuento = request.form.get('descuento')
    stock = request.form['stock']
    nombredeTienda = request.form['nombredeTienda']
    descripcion = request.form['descripcion']
    caracteristicas = request.form['caracteristicas']
    idCategoria = request.form['idCategoria']
    
    # Manejo de la imagen
    if 'imagen' not in request.files:
        flash('No se subió ningún archivo', 'error')
        return redirect(request.url)
    
    file = request.files['imagen']
    
    if file and allowed_file(file.filename):
        # Asegurarse de que el nombre del archivo es seguro
        filename = secure_filename(file.filename)
        
        # Guardar la imagen en la carpeta de uploads (static/img)
        file.save(os.path.join(producto_bp.config['UPLOAD_FOLDER'], filename))
        
        # Registrar el producto en la base de datos, almacenando la ruta de la imagen
        controlador_productos.agregar_producto(
            nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, filename
        )
        
        flash('Producto registrado exitosamente', 'success')
        return redirect(url_for('producto_bp.menu_man_producto'))
    else:
        flash('Formato de archivo no permitido. Solo se permiten archivos .webp', 'error')
        return redirect(request.url)

# Ruta para actualizar un producto
@producto_bp.route('/actualizar_producto', methods=["POST"])
def actualizar_producto():
    idProducto = request.form.get('idProducto')
    nombredeproducto = request.form.get('nombredeproducto')
    autor = request.form.get('autor')
    precio = request.form.get('precio')
    descuento = request.form.get('descuento')
    stock = request.form.get('stock')
    nombredeTienda = request.form.get('nombredeTienda')
    descripcion = request.form.get('descripcion')
    caracteristicas = request.form.get('caracteristicas')
    idCategoria = request.form.get('idCategoria')

    # Obtener la imagen actual del producto
    producto = controlador_productos.obtener_producto_por_id(idProducto)
    imagen_actual = producto[10]  # El índice correcto para la imagen en la tupla

    # Manejo de la nueva imagen (si se subió una nueva)
    if 'imagen' in request.files:
        file = request.files['imagen']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(producto_bp.config['UPLOAD_FOLDER'], filename))
        else:
            filename = imagen_actual  # Mantener la imagen actual si no se subió una nueva imagen
    else:
        filename = imagen_actual

    try:
        controlador_productos.actualizar_producto(idProducto, nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, filename)
        flash("Producto actualizado exitosamente", "success")
    except Exception as e:
        flash(f"Error al actualizar producto: {str(e)}", "error")

    return redirect(url_for('producto_bp.menu_man_producto'))



# Ruta para eliminar un producto
@producto_bp.route('/eliminar_producto/<int:idProducto>', methods=["POST"])
def eliminar_producto(idProducto):
    try:
        controlador_productos.eliminar_producto(idProducto)
        flash("Producto eliminado exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar producto: {str(e)}", "error")
    
    return redirect(url_for('producto_bp.menu_man_producto'))
