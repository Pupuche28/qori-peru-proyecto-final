from bd import obtener_conexion

def obtener_todas_tarjetas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT T.idTarjeta, T.nombre, T.nroTarjeta, T.fecha, U.nombres, T.idUsuario 
        FROM TARJETA T 
        JOIN USUARIO U ON T.idUsuario = U.idUsuario
        ORDER BY T.idTarjeta ASC
    """)
    tarjetas = cursor.fetchall()
    conexion.close()
    return tarjetas

def agregar_tarjeta(nombre, nroTarjeta, fecha, idUsuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO TARJETA (nombre, nroTarjeta, fecha, idUsuario) VALUES (%s, %s, %s, %s)", 
                   (nombre, nroTarjeta, fecha, idUsuario))
    conexion.commit()
    conexion.close()

def actualizar_tarjeta(idTarjeta, nombre, nroTarjeta, fecha, idUsuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE TARJETA SET nombre = %s, nroTarjeta = %s, fecha = %s, idUsuario = %s WHERE idTarjeta = %s", 
                   (nombre, nroTarjeta, fecha, idUsuario, idTarjeta))
    conexion.commit()
    conexion.close()

def eliminar_tarjeta(idTarjeta):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM TARJETA WHERE idTarjeta = %s", (idTarjeta,))
    conexion.commit()
    conexion.close()

def obtener_todos_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT idUsuario, nombres FROM USUARIO")
    usuarios = cursor.fetchall()
    conexion.close()
    return usuarios