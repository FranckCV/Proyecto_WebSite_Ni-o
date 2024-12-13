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