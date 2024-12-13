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
                SUM(CASE WHEN s.estado = 1 THEN 1 ELSE 0 END) - 
                SUM(CASE WHEN s.estado = 0 THEN 1 ELSE 0 END) AS suma_estado
                FROM seleccion s
                JOIN agrupacion a ON s.AGRUPACIONGRUPOid = a.GRUPOid AND s.AGRUPACIONCUALIDADid = a.CUALIDADid
                JOIN cualidad c ON a.CUALIDADid = c.id
                JOIN elemento e ON c.ELEMENTOid = e.id
                WHERE s.PARTICIPANTEid = %s
                GROUP BY e.nomElemento
                ORDER BY e.nomElemento;
            """
            cursor.execute(sql, participante_id)
            pruebita = cursor.fetchall() 
        conexion.close()
        return pruebita
    except Exception as e:
        return e
    
def verificar_cantidad_seleccionada(participante_id, grupo_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM seleccion WHERE participanteid = %s AND agrupaciongrupoid = %s"
            cursor.execute(sql, (participante_id, grupo_id))
            cantidad = cursor.fetchone()[0]
            
            return cantidad == 2
          
    except Exception as e:
        print(f"Error al verificar la cantidad seleccionada: {e}")
        return False  
    conexion.close()  
