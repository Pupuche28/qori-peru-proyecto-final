from bd import obtener_conexion
from werkzeug.security import check_password_hash
from flask_login import UserMixin
import traceback

# Clase Usuario que extiende de UserMixin para trabajar con Flask-Login
class Usuario(UserMixin):
    def __init__(self, id, nombres, apellidos, email, idRol):
        self.id = id  # Aquí usas 'id' en lugar de 'idUsuario'
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.idRol = idRol  # Asegúrate de incluir el idRol como atributo



# Modificación de la verificación de usuario sin hasheo de contraseñas
def verificar_usuario(email, contrasena):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Consulta para obtener el usuario desde la base de datos usando el email
            sql = "SELECT * FROM USUARIO WHERE email = %s"
            cursor.execute(sql, (email,))
            usuario_db = cursor.fetchone()

        conexion.close()

        # Verificar si el usuario fue encontrado
        if usuario_db is None:
            print(f"Usuario no encontrado para el correo {email}")
            return None

        # Comparar la contraseña ingresada directamente con la contraseña almacenada
        if usuario_db[6] == contrasena:  # usuario_db[6] es la columna de contraseñas
            print(f"Contraseña correcta para el usuario {email}")
            return Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3], usuario_db[8])  # usuario_db[8] es el idRol
        else:
            print(f"Contraseña incorrecta para el usuario {email}")
            return None
    except Exception as e:
        print(f"Error en la función verificar_usuario: {str(e)}")
        print(traceback.format_exc())
        return None
