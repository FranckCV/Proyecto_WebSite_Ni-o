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
                select a.cualidadid, c.nombre, c.descripcion 
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


def obtener_grupo_incompleto(participante_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
                SELECT g.id
                FROM grupo g
                LEFT JOIN (
                    SELECT s.AGRUPACIONGRUPOid, COUNT(*) AS seleccionadas
                    FROM seleccion s
                    WHERE s.PARTICIPANTEid = %s
                    GROUP BY s.AGRUPACIONGRUPOid
                ) AS conteo
                ON g.id = conteo.AGRUPACIONGRUPOid
                WHERE IFNULL(conteo.seleccionadas, 0) < (SELECT COUNT(*) FROM agrupacion WHERE GRUPOid = g.id)
                LIMIT 1;
            """
            cursor.execute(sql, (participante_id,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener el grupo incompleto: {str(e)}")
        return None
    finally:
        conexion.close()


def obtener_cantidad_maxima_progreso():
    conexion = obtener_conexion()
    # try:
    with conexion.cursor() as cursor:
        sql= "select count(*) from grupo"
        cursor.execute(sql)
        grupos = cursor.fetchone()
        numero = grupos[0] * 2
    conexion.close()
    return numero
    # except Exception as e:
    #     return e
    



