from controladores.bd import obtener_conexion

def obtener_resultados():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql= '''
            SELECT 
                p.id,
                p.nombres,
                TIMESTAMPDIFF(YEAR, p.fecha_nacimiento, CURDATE()) AS edad,
                p.telefono,
                p.correo,
                p.fecha_registro,
                SUM(CASE WHEN e.id = 1 THEN s.estado ELSE 0 END) AS resultado_Fuego,
                SUM(CASE WHEN e.id = 3 THEN s.estado ELSE 0 END) AS resultado_Aire,
                SUM(CASE WHEN e.id = 2 THEN s.estado ELSE 0 END) AS resultado_Agua,
                SUM(CASE WHEN e.id = 4 THEN s.estado ELSE 0 END) AS resultado_Tierra
            FROM 
                seleccion s
            INNER JOIN 
                agrupacion a ON s.AGRUPACIONGRUPOid = a.GRUPOid AND s.AGRUPACIONCUALIDADid = a.CUALIDADid
            INNER JOIN 
                cualidad c ON a.CUALIDADid = c.id
            INNER JOIN 
                elemento e ON c.ELEMENTOid = e.id
            INNER JOIN 
                participante p ON s.PARTICIPANTEid = p.id
            GROUP BY 
                p.id, p.nombres
            ORDER BY 
                p.id;
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
    conexion.close()
    return result
   
    
def insertar_participante(nombres, fecha_nacimiento, telefono, correo):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO participante (nombres, fecha_nacimiento, telefono, correo, fecha_registro)
                VALUES (%s, %s, %s, %s, NOW());
            """
            
            cursor.execute(sql, (nombres, fecha_nacimiento, telefono, correo))
            conexion.commit()
            participante_id = cursor.lastrowid
            
        conexion.close()
        return participante_id
    except Exception as e:
        conexion.close()
        return f"Error al insertar participante: {str(e)}"

def buscar_participante(id_participante):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql= '''
            SELECT * from participante where id = %s;
        '''
        cursor.execute(sql, (id_participante))
        result = cursor.fetchone()
    conexion.close()
    return result
