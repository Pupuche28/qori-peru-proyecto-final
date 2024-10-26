from bd import obtener_conexion

def agregar_tarjeta(nombre, nro_tarjeta, fecha, ccv, id_usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO TARJETA (nombre, nroTarjeta, fecha, ccv, idUsuario)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, nro_tarjeta, fecha, ccv, id_usuario))
    conexion.commit()
    conexion.close()

def obtener_tarjetas(idUsuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        consulta = "SELECT idTarjeta, nombre, nroTarjeta, fecha FROM TARJETA WHERE idUsuario = %s"
        cursor.execute(consulta, (idUsuario,))
        tarjetas = cursor.fetchall()
    conexion.close()
    
    # Verificación temporal
    print(f"Tarjetas obtenidas para el usuario {idUsuario}: {tarjetas}")
    
    return tarjetas