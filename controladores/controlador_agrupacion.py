from controladores.bd import obtener_conexion
def obtener_cantidad_grupo():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql= "select id, nomgrupo from grupo"
            cursor.execute(sql)
            grupos = cursor.fetchall()
        conexion.close()
        return grupos
    except Exception as e:
        return e
    
def obtener_cualidades(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
                select a.cualidadid, c.nombre 
                from agrupacion a
                inner join cualidad c on c.id = a.CUALIDADid
                where a.grupoid = %s
            """
            cursor.execute(sql, (id,))
            cualidades = cursor.fetchall() 
        conexion.close()
        return cualidades
    except Exception as e:
        return e
