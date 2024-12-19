from controladores.bd import obtener_conexion

def insertar_seleccion(participante_id, grupo_id, cualidad_id,estado):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql_select = """
                SELECT * 
                FROM seleccion 
                WHERE PARTICIPANTEid = %s AND AGRUPACIONGRUPOid = %s AND AGRUPACIONCUALIDADid = %s
            """
            cursor.execute(sql_select, (participante_id, grupo_id, cualidad_id))
            cantidad = cursor.rowcount

            if cantidad == 1:
                sql_delete = """
                    DELETE FROM seleccion 
                    WHERE PARTICIPANTEid = %s AND AGRUPACIONGRUPOid = %s AND AGRUPACIONCUALIDADid = %s
                """
                cursor.execute(sql_delete, (participante_id, grupo_id, cualidad_id))
                mensaje = "Selección eliminada correctamente."
            else:
                sql_insert = """
                    INSERT INTO seleccion (PARTICIPANTEid, AGRUPACIONGRUPOid, AGRUPACIONCUALIDADid, estado) 
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql_insert, (participante_id, grupo_id, cualidad_id, estado))
                mensaje = "Selección insertada correctamente."

        conexion.commit()
        conexion.close()

        return mensaje

    except Exception as e:
        return f"Error al procesar la selección: {e}"
    

def llenar_grafico_barras(participante_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
                SELECT
                    e.nomElemento,
                    COALESCE(SUM(CASE WHEN s.estado = 1 THEN 1 ELSE 0 END), 0) - 
                    COALESCE(SUM(CASE WHEN s.estado = 0 THEN 1 ELSE 0 END), 0) AS suma_estado
                FROM elemento e
                LEFT JOIN cualidad c ON e.id = c.ELEMENTOid
                LEFT JOIN agrupacion a ON c.id = a.CUALIDADid
                LEFT JOIN seleccion s ON a.GRUPOid = s.AGRUPACIONGRUPOid AND a.CUALIDADid = s.AGRUPACIONCUALIDADid AND s.PARTICIPANTEid = %s
                GROUP BY e.nomElemento
                ORDER BY 
                    CASE 
                        WHEN e.nomElemento = 'Fuego' THEN 1
                        WHEN e.nomElemento = 'Aire' THEN 2
                        WHEN e.nomElemento = 'Agua' THEN 3
                        WHEN e.nomElemento = 'Tierra' THEN 4
                        ELSE 5 -- En caso de que haya un elemento no esperado
                    END;
            """
            cursor.execute(sql, (participante_id,))
            resultado = cursor.fetchall()
        conexion.close()
        return resultado
    except Exception as e:
        return e


def verificar_cantidad_seleccionada(participante_id, grupo_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM seleccion WHERE participanteid = %s AND agrupaciongrupoid = %s"
            cursor.execute(sql, (participante_id, grupo_id))
            cantidad = cursor.fetchone()[0]
        conexion.close()      
        return cantidad == 2  
    except Exception as e:
        print(f"Error al verificar la cantidad seleccionada: {e}")
        return False  


def obtener_id_cualidad_positiva_seleccionada(participante_id, grupo_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT agrupacioncualidadid FROM seleccion WHERE participanteid = %s AND agrupaciongrupoid = %s and estado = true"
            cursor.execute(sql, (participante_id, grupo_id))
            seleccion = cursor.fetchone()
        conexion.close()      
        return seleccion[0] if seleccion else None  
    except Exception as e:
        print(f"Error al verificar la cantidad seleccionada: {e}")
        return False  


def obtener_id_cualidad_negativa_seleccionada(participante_id, grupo_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT agrupacioncualidadid FROM seleccion WHERE participanteid = %s AND agrupaciongrupoid = %s and estado = false"
            cursor.execute(sql, (participante_id, grupo_id))
            seleccion = cursor.fetchone()
        conexion.close()      
        return seleccion[0] if seleccion else None 
    except Exception as e:
        print(f"Error al verificar la cantidad seleccionada: {e}")
        return False  


def obtener_ultima_seleccion(participante_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT max(agrupaciongrupoid) FROM seleccion WHERE participanteid = %s "
            cursor.execute(sql, (participante_id,))
            ultima_seleccion = cursor.fetchone()
        conexion.close()      
        return ultima_seleccion[0] if ultima_seleccion else None 
    except Exception as e:
        print(f"Error al verificar la cantidad seleccionada: {e}")
        return False  


def contar_selecciones_por_participante(participante_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
                SELECT COUNT(*) 
                FROM seleccion 
                WHERE PARTICIPANTEid = %s;
            """
            cursor.execute(sql, (participante_id,))
            resultado = cursor.fetchone()
            cantidad = resultado[0] if resultado else 0
        conexion.close()
        return cantidad
    except Exception as e:
        conexion.close()
        return f"Error al contar selecciones: {str(e)}"


def eliminar_seleccion_idpar(participante_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = ''' delete from seleccion where PARTICIPANTEid = '''+str(participante_id)+''' ; '''
        cursor.execute(sql)
    conexion.commit()
    conexion.close()


