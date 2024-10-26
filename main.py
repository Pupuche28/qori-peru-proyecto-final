from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from routes.usuario_routes import usuario_bp  # Importar el blueprint de usuario
from routes.autenticacion_routes import autenticacion_bp  # Importar el blueprint de autenticación
from routes.admin_routes import admin_bp
from routes.rol_routes import rol_bp
from routes.resenas_routes import resena_bp  # Importar el blueprint de reseñas
from routes.categoria_routes import categoria_bp
from routes.producto_routes import producto_bp  # Importar el blueprint de productos
from routes.ceramica_routes import ceramica_bp
from routes.joyeria_routes import joyeria_bp
from routes.retablos_routes import retablos_bp
from routes.textiles_routes import textiles_bp
from routes.detalleproducto_routes import detalle_producto_bp
from routes.carrito_routes import carrito_bp  # Importar el blueprint del carrito
from routes.tipoentrega_routes import tipo_entrega_bp
from routes.tarjeta_routes import tarjeta_bp
from routes.tipopago_routes import tipopago_bp
from routes.mispedidos_routes import mispedidos_bp
from routes.tarjetasAdmin_routes import tarjetaAdmin_bp
from routes.pedido_routes import pedido_bp


from controllers.controlador_ceramica import obtener_productos_ceramica
import controllers.controlador_tipoentrega as controlador_tipoentrega
from controllers.controlador_detalleproducto import obtener_producto_por_id



import controllers.controlador_resenas as controlador_resenas  
import controllers.controlador_usuarios as controlador_usuarios  # Controlador para usuarios



app = Flask(__name__)

# Agregar una clave secreta para las sesiones
app.secret_key = 'rodrigho'  # Clave secreta para las sesiones

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'autenticacion_bp.login'  # Redirigir a la página de login si no ha iniciado sesión


# Función para cargar usuario desde el ID de sesión
@login_manager.user_loader
def load_user(user_id):
    return controlador_usuarios.obtener_usuario_por_id(user_id)



# Context processor: Hacer disponible `current_user` en todas las plantillas
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Registrar el blueprint de usuario y autenticación
app.register_blueprint(usuario_bp, url_prefix="/usuario")
app.register_blueprint(autenticacion_bp, url_prefix="/auth")  # Registrar las rutas de autenticación
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(rol_bp, url_prefix="/rol")
app.register_blueprint(categoria_bp, url_prefix="/categoria")
app.register_blueprint(resena_bp, url_prefix="/resena")  # Registrar las rutas de reseñas
app.register_blueprint(producto_bp, url_prefix='/producto')
app.register_blueprint(ceramica_bp)
app.register_blueprint(joyeria_bp)
app.register_blueprint(retablos_bp)
app.register_blueprint(textiles_bp)
app.register_blueprint(detalle_producto_bp)
app.register_blueprint(carrito_bp, url_prefix='/carrito')
app.register_blueprint(tipo_entrega_bp)
app.register_blueprint(tarjeta_bp, url_prefix='/tarjetas')
app.register_blueprint(tipopago_bp)
app.register_blueprint(mispedidos_bp)
app.register_blueprint(tarjetaAdmin_bp, url_prefix='/tarjetasAdmin')
app.register_blueprint(pedido_bp, url_prefix='/pedidos')




# Redirigir a la página de administrador si el usuario tiene rol de administrador
@app.route("/")
def home():
    # Verificar si el usuario está autenticado
    if current_user.is_authenticated:
        # Si el usuario es administrador (idRol = 1)
        if current_user.idRol == 1:  # 1 es el idRol para "administrador"
            return render_template("menuAdministrador.html")  # Redirigir al menú del administrador
        else:
            return render_template("index.html")  # Si no es administrador, mostrar el home normal
    else:
        return render_template("index.html")  # Si no está autenticado, mostrar el home normal

# Página del administrador
@app.route("/admin")
@login_required
def admin_home():
    # Verifica que el usuario sea administrador antes de mostrar la página
    if current_user.idRol == 1:  # 1 es el rol de administrador
        return render_template("menuAdministrador.html")
    else:
        return redirect(url_for("home"))  # Si no es administrador, redirigir a la página principal

# Ruta para la página "cambios.html"
@app.route("/cambios")
def cambios():
    return render_template("cambios.html")

# Ruta para la página "carrito.html"
@app.route("/carrito")
@login_required
def carrito():
    return render_template("carrito.html")

# Ruta para la página "ceramica.html"
@app.route('/ceramica')
def ceramica():
    productos_ceramica = obtener_productos_ceramica()  # Obtiene los productos de cerámica
    return render_template('ceramica.html', productos=productos_ceramica)


# Ruta para la página "contactos.html"
@app.route("/contactos")
def contactos():
    return render_template("contactos.html")

# Ruta para la página "joyeria.html"
@app.route("/joyeria")
def joyeria():
    return render_template("joyeria.html")

# Ruta para la página "legales.html"
@app.route("/legales")
def legales():
    return render_template("legales.html")

# Ruta para la página "nosotros.html"
@app.route("/nosotros")
def nosotros():
    resenas = controlador_resenas.obtener_todas_resenas()
    return render_template("nosotros.html", resenas=resenas)

# Ruta para la página "politicas.html"
@app.route("/politicas")
def politicas():
    return render_template("politicas.html")

# Ruta para la página "preguntas.html"
@app.route("/preguntas")
def preguntas():
    return render_template("preguntas.html")

# Ruta para la página "productodetalle.html"
@app.route('/producto/<int:id_producto>')
def productodetalle(id_producto):
    # Obtener el producto por su ID
    producto = obtener_producto_por_id(id_producto)
    
    # Verificar si el producto fue encontrado
    if producto:
        # Pasar el producto a la plantilla
        return render_template('productodetalle.html', producto=producto)
    else:
        # Manejar el caso en el que el producto no existe
        return "Producto no encontrado", 404


# Ruta para la página "registrate.html"
@app.route("/registrate")
def registrate():
    return render_template("registrate.html")

# Ruta para la página "retablos.html"
@app.route("/retablos")
def retablos():
    return render_template("retablos.html")

# Ruta para la página "terminos.html"
@app.route("/terminos")
def terminos():
    return render_template("terminos.html")

# Ruta para la página "textiles.html"
@app.route("/textiles")
def textiles():
    return render_template("textiles.html")

# Ruta para la página "tipoentrega.html"
@app.route("/tipoentrega")
@login_required  # Asegurarse de que el usuario esté autenticado
def tipoentrega():
    # Obtener la dirección del usuario desde el controlador
    direccion = controlador_tipoentrega.obtener_direccion_usuario(current_user.id)

    # Renderizar la plantilla pasando la dirección del usuario
    return render_template("tipoentrega.html", direccion=direccion)


# Ruta para la página "tipopago.html"
@app.route("/tipopago")
def tipopago():
    return render_template("tipopago.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
