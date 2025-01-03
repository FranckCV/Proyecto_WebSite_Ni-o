from controladores.bd import obtener_conexion

def cambiar_contrasenia(user, contrasenia):
    # Verificar si los valores son None
    if user is None or contrasenia is None:
        print("Error: El usuario o la contraseña no pueden ser None")
        return

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "update administrador set clave = %s where usuario = %s"
            
            # Imprimir los valores para verificar si son correctos
            print(f"Ejecutando SQL: {sql} con valores: {contrasenia}, {user}")
            
            cursor.execute(sql, (contrasenia, user))
        conexion.commit()
    except Exception as e:
        print(e)

def obtener_clave(user):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "select clave from administrador where usuario=%s"
            cursor.execute(sql,(user))
            clave = cursor.fetchone()
            if clave:
                return clave[0]  # Accede al primer elemento de la tupla
            else:
                return "No se encontraron resultados"
    except Exception as e:
        print(e)