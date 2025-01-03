from controladores.bd import obtener_conexion

def cambiar_contrasenia(user,contrasenia):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "update administrador set clave =%s where user=%s"
            cursor.execute(sql,(contrasenia,user))
    except Exception as e:
        print(e)
    
def obtener_clave(user):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "select clave from administrador where user=%s"
            cursor.execute(sql,(user))
    except Exception as e:
        print(e)