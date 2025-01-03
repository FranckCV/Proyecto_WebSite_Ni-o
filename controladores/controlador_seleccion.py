from controladores.bd import obtener_conexion

def insertar_seleccion_positiva(participante_id, grupo_id, cualidad_id, estado):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Verificar si ya existe una selección positiva
            sql_verificar_positiva = """
                SELECT * 
                FROM seleccion 
                WHERE PARTICIPANTEid = %s AND AGRUPACIONGRUPOid = %s AND estado = 1
            """
            cursor.execute(sql_verificar_positiva, (participante_id, grupo_id))
            positivo = cursor.fetchone()  

            # Verificar si ya existe una selección negativa con la misma cualidad
            sql_verificar_negativo = """
                SELECT * 
                FROM seleccion 
                WHERE PARTICIPANTEid = %s AND AGRUPACIONGRUPOid = %s AND AGRUPACIONCUALIDADid = %s AND estado = 0
            """
            cursor.execute(sql_verificar_negativo, (participante_id, grupo_id, cualidad_id))
            negativo = cursor.fetchone() 

            # Eliminar la selección positiva si ya existe
            if positivo:
                sql_delete = """
                    DELETE FROM seleccion 
                    WHERE PARTICIPANTEid = %s AND AGRUPACIONGRUPOid = %s AND estado = 1
                """
                cursor.execute(sql_delete, (participante_id, grupo_id))

                if positivo[2] == int(cualidad_id):
                    conexion.commit()
                    return "Selección positiva para id repetido eliminada correctamente."
                
                mensaje = "Selección positiva eliminada correctamente."
            
            # Eliminar la selección negativa si ya existe
            if negativo :
                sql_delete = """
                    DELETE FROM seleccion 
                    WHERE PARTICIPANTEid = %s AND AGRUPACIONGRUPOid = %s AND AGRUPACIONCUALIDADid = %s AND estado = 0
                """
                cursor.execute(sql_delete, (participante_id, grupo_id, cualidad_id))
                mensaje = "Selección negativa eliminada correctamente."
            
            # Insertar la selección positiva
            sql_insert = """
                INSERT INTO seleccion (PARTICIPANTEid, AGRUPACIONGRUPOid, AGRUPACIONCUALIDADid, estado) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (participante_id, grupo_id, cualidad_id, estado))
            mensaje = "Selección positiva insertada correctamente."

        conexion.commit()
        return mensaje

    except Exception as e:
        return f"Error al procesar la selección positiva: {e}"



def insertar_seleccion_negativa(participante_id, grupo_id, cualidad_id, estado):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Verificar si ya existe una selección negativa
            sql_verificar_negativo = """
                SELECT * 
                FROM seleccion 
                WHERE PARTICIPANTEid = %s AND AGRUPACIONGRUPOid = %s AND estado = 0
            """
            cursor.execute(sql_verificar_negativo, (participante_id, grupo_id))
            negativo = cursor.fetchone() 

            # Verificar si ya existe una selección positiva con la misma cualidad
            sql_verificar_positivo = """
                SELECT * 
                FROM seleccion 
                WHERE PARTICIPANTEid = %s AND AGRUPACIONGRUPOid = %s AND AGRUPACIONCUALIDADid = %s AND estado = 1
            """
            cursor.execute(sql_verificar_positivo, (participante_id, grupo_id, cualidad_id))
            positivo = cursor.fetchone() 

            # Eliminar la selección negativa si ya existe
            if negativo :
                sql_delete = """
                    DELETE FROM seleccion 
                    WHERE PARTICIPANTEid = %s AND AGRUPACIONGRUPOid = %s AND estado = 0
                """
                cursor.execute(sql_delete, (participante_id, grupo_id))
                if negativo[2] == int(cualidad_id):
                    conexion.commit()
                    return "Selección positiva para id repetido eliminada correctamente."
                mensaje = "Selección negativa eliminada correctamente."
            
            # Eliminar la selección positiva si ya existe
            if positivo:
                sql_delete = """
                    DELETE FROM seleccion 
                    WHERE PARTICIPANTEid = %s AND AGRUPACIONGRUPOid = %s AND AGRUPACIONCUALIDADid = %s AND estado = 1
                """
                cursor.execute(sql_delete, (participante_id, grupo_id, cualidad_id))
                mensaje = "Selección positiva eliminada correctamente."
            
            # Insertar la selección negativa
            sql_insert = """
                INSERT INTO seleccion (PARTICIPANTEid, AGRUPACIONGRUPOid, AGRUPACIONCUALIDADid, estado) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (participante_id, grupo_id, cualidad_id, estado))
            mensaje = "Selección negativa insertada correctamente."

        conexion.commit()
        return mensaje

    except Exception as e:
        return f"Error al procesar la selección negativa: {e}"



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


