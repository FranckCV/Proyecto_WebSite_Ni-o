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


def funcion_prueba_jpd():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
                SELECT e.id AS ElementoID, e.nomElemento AS Elemento, COUNT(c.id) AS CantidadCualidades
                FROM elemento e
                LEFT JOIN cualidad c ON e.id = c.ELEMENTOid
                GROUP BY e.id, e.nomElemento;
            """
            cursor.execute(sql)
            pruebita = cursor.fetchall() 
        conexion.close()
        return pruebita
    except Exception as e:
        return e
