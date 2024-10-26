from flask import Blueprint, render_template, request, redirect, url_for, flash
import controllers.controlador_pedido as controlador_pedido

# Crear el Blueprint para pedidos
pedido_bp = Blueprint('pedido_bp', __name__)

# Ruta para mostrar la página de gestión de pedidos
@pedido_bp.route('/menu_man_pedido', methods=["GET"])
def menu_man_pedido():
    pedidos = controlador_pedido.obtener_todos_pedidos()
    usuarios = controlador_pedido.obtener_todos_usuarios()
    return render_template('menuManPedido.html', pedidos=pedidos, usuarios=usuarios)

# Ruta para agregar un nuevo pedido
@pedido_bp.route('/agregar_pedido', methods=["POST"])
def agregar_pedido():
    fechainicio = request.form.get('fechainicio')
    idUsuario = request.form.get('idUsuario')
    
    if not fechainicio or not idUsuario:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('pedido_bp.menu_man_pedido'))

    try:
        controlador_pedido.agregar_pedido(fechainicio, idUsuario)
        flash("Pedido agregado exitosamente", "success")
    except Exception as e:
        flash(f"Error al agregar pedido: {str(e)}", "error")
    
    return redirect(url_for('pedido_bp.menu_man_pedido'))

# Ruta para actualizar un pedido
@pedido_bp.route('/actualizar_pedido', methods=["POST"])
def actualizar_pedido():
    idPedido = request.form.get('idPedido')
    fechainicio = request.form.get('fechainicio')
    fechafinalizado = request.form.get('fechafinalizado')
    estado = request.form.get('estado')
    idUsuario = request.form.get('idUsuario')
    
    if not idPedido or not fechainicio or not estado or not idUsuario:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for('pedido_bp.menu_man_pedido'))

    try:
        controlador_pedido.actualizar_pedido(idPedido, fechainicio, fechafinalizado, estado, idUsuario)
        flash("Pedido actualizado exitosamente", "success")
    except Exception as e:
        flash(f"Error al actualizar pedido: {str(e)}", "error")

    return redirect(url_for('pedido_bp.menu_man_pedido'))

# Ruta para eliminar un pedido
@pedido_bp.route('/eliminar_pedido/<int:idPedido>', methods=["POST"])
def eliminar_pedido(idPedido):
    try:
        controlador_pedido.eliminar_pedido(idPedido)
        flash("Pedido eliminado exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar pedido: {str(e)}", "error")
    
    return redirect(url_for('pedido_bp.menu_man_pedido'))
