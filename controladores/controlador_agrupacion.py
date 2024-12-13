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
                select g.nomgrupo, c.nombre 
                from agrupacion a
                inner join grupo g on g.id = a.GRUPOid
                inner join cualidad c on c.id = a.CUALIDADid
                where g.id = %s
            """
            cursor.execute(sql, (id,))
            cualidades = cursor.fetchall() 
        conexion.close()
        return cualidades
    except Exception as e:
        return e
