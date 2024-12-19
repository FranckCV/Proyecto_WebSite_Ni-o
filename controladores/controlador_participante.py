from controladores.bd import obtener_conexion

def obtener_resultadosxd():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql= '''
            SELECT 
                p.id,
                p.nombres,
                p.apellidos,
                COUNT(DISTINCT s.AGRUPACIONGRUPOid) AS grupos_seleccionados,
                p.id,
                p.telefono,
                p.correo,
                p.id,
                p.id,
                p.id,
                p.id,
                p.id                
            FROM 
                participante p
            LEFT JOIN 
                seleccion s ON s.PARTICIPANTEid = p.id
            LEFT JOIN 
                agrupacion a ON s.AGRUPACIONGRUPOid = a.GRUPOid AND s.AGRUPACIONCUALIDADid = a.CUALIDADid
            LEFT JOIN 
                cualidad c ON a.CUALIDADid = c.id
            LEFT JOIN 
                elemento e ON c.ELEMENTOid = e.id
            GROUP BY 
                p.id, p.nombres
            ORDER BY 
                p.fecha_registro , grupos_seleccionados ;
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
    conexion.close()
    return result


def obtener_resultados_2():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql= '''
            SELECT 
                p.id,
                p.nombres,
                p.apellidos,
                COUNT(DISTINCT s.AGRUPACIONGRUPOid) AS grupos_seleccionados,
                TIMESTAMPDIFF(YEAR, p.fecha_nacimiento, CURDATE()) AS edad,
                p.telefono,
                p.correo,
                p.fecha_registro,
                SUM(CASE WHEN e.id = 1 THEN s.estado ELSE 0 END) AS resultado_Fuego,
                SUM(CASE WHEN e.id = 3 THEN s.estado ELSE 0 END) AS resultado_Aire,
                SUM(CASE WHEN e.id = 2 THEN s.estado ELSE 0 END) AS resultado_Agua,
                SUM(CASE WHEN e.id = 4 THEN s.estado ELSE 0 END) AS resultado_Tierra
            FROM 
                participante p
            LEFT JOIN 
                seleccion s ON s.PARTICIPANTEid = p.id
            LEFT JOIN 
                agrupacion a ON s.AGRUPACIONGRUPOid = a.GRUPOid AND s.AGRUPACIONCUALIDADid = a.CUALIDADid
            LEFT JOIN 
                cualidad c ON a.CUALIDADid = c.id
            LEFT JOIN 
                elemento e ON c.ELEMENTOid = e.id
            GROUP BY 
                p.id, p.nombres
            ORDER BY 
                p.fecha_registro , grupos_seleccionados ;
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
    conexion.close()
    return result


def obtener_resultados():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql= '''
            SELECT 
                p.id,
                p.nombres,
                p.apellidos,
                COUNT( s.AGRUPACIONCUALIDADid) AS grupos_seleccionados,
                TIMESTAMPDIFF(YEAR, p.fecha_nacimiento, CURDATE()) AS edad,
                p.telefono,
                p.correo,
                p.fecha_registro,
                COUNT(CASE WHEN e.id = 1 AND s.estado = 1 THEN 1 END) AS fuego_estado_1,
                COUNT(CASE WHEN e.id = 1 AND s.estado = 0 THEN 1 END) AS fuego_estado_0,
                COUNT(CASE WHEN e.id = 2 AND s.estado = 1 THEN 1 END) AS agua_estado_1,
                COUNT(CASE WHEN e.id = 2 AND s.estado = 0 THEN 1 END) AS agua_estado_0,
                COUNT(CASE WHEN e.id = 3 AND s.estado = 1 THEN 1 END) AS aire_estado_1,
                COUNT(CASE WHEN e.id = 3 AND s.estado = 0 THEN 1 END) AS aire_estado_0,
                COUNT(CASE WHEN e.id = 4 AND s.estado = 1 THEN 1 END) AS tierra_estado_1,
                COUNT(CASE WHEN e.id = 4 AND s.estado = 0 THEN 1 END) AS tierra_estado_0
            FROM 
                participante p
            LEFT JOIN 
                seleccion s ON s.PARTICIPANTEid = p.id
            LEFT JOIN 
                agrupacion a ON s.AGRUPACIONGRUPOid = a.GRUPOid AND s.AGRUPACIONCUALIDADid = a.CUALIDADid
            LEFT JOIN 
                cualidad c ON a.CUALIDADid = c.id
            LEFT JOIN 
                elemento e ON c.ELEMENTOid = e.id
            GROUP BY 
                p.id, p.nombres, p.apellidos, p.telefono, p.correo, p.fecha_registro
            ORDER BY 
                grupos_seleccionados , p.fecha_registro
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
    conexion.close()
    return result

def obtener_resultado_id(par_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql= '''
            SELECT 
                p.id,
                p.nombres,
                p.apellidos,
                COUNT( s.AGRUPACIONCUALIDADid) AS grupos_seleccionados,
                TIMESTAMPDIFF(YEAR, p.fecha_nacimiento, CURDATE()) AS edad,
                p.telefono,
                p.correo,
                p.fecha_registro,
                COUNT(CASE WHEN e.id = 1 AND s.estado = 1 THEN 1 END) AS fuego_estado_1,
                COUNT(CASE WHEN e.id = 1 AND s.estado = 0 THEN 1 END) AS fuego_estado_0,
                COUNT(CASE WHEN e.id = 2 AND s.estado = 1 THEN 1 END) AS agua_estado_1,
                COUNT(CASE WHEN e.id = 2 AND s.estado = 0 THEN 1 END) AS agua_estado_0,
                COUNT(CASE WHEN e.id = 3 AND s.estado = 1 THEN 1 END) AS aire_estado_1,
                COUNT(CASE WHEN e.id = 3 AND s.estado = 0 THEN 1 END) AS aire_estado_0,
                COUNT(CASE WHEN e.id = 4 AND s.estado = 1 THEN 1 END) AS tierra_estado_1,
                COUNT(CASE WHEN e.id = 4 AND s.estado = 0 THEN 1 END) AS tierra_estado_0,
                p.fecha_nacimiento
            FROM 
                participante p
            LEFT JOIN 
                seleccion s ON s.PARTICIPANTEid = p.id
            LEFT JOIN 
                agrupacion a ON s.AGRUPACIONGRUPOid = a.GRUPOid AND s.AGRUPACIONCUALIDADid = a.CUALIDADid
            LEFT JOIN 
                cualidad c ON a.CUALIDADid = c.id
            LEFT JOIN 
                elemento e ON c.ELEMENTOid = e.id
            WHERE 
                p.id = '''+str(par_id)+'''
            GROUP BY 
                p.id, p.nombres, p.apellidos, p.telefono, p.correo, p.fecha_registro
            ORDER BY 
                grupos_seleccionados , p.fecha_registro
        '''
        cursor.execute(sql)
        result = cursor.fetchone()
    conexion.close()
    return result



def buscar_resultado_nombre(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql= '''
            SELECT 
                p.id,
                p.nombres,
                p.apellidos,
                COUNT( s.AGRUPACIONCUALIDADid) AS grupos_seleccionados,
                TIMESTAMPDIFF(YEAR, p.fecha_nacimiento, CURDATE()) AS edad,
                p.telefono,
                p.correo,
                p.fecha_registro,
                COUNT(CASE WHEN e.id = 1 AND s.estado = 1 THEN 1 END) AS fuego_estado_1,
                COUNT(CASE WHEN e.id = 1 AND s.estado = 0 THEN 1 END) AS fuego_estado_0,
                COUNT(CASE WHEN e.id = 2 AND s.estado = 1 THEN 1 END) AS agua_estado_1,
                COUNT(CASE WHEN e.id = 2 AND s.estado = 0 THEN 1 END) AS agua_estado_0,
                COUNT(CASE WHEN e.id = 3 AND s.estado = 1 THEN 1 END) AS aire_estado_1,
                COUNT(CASE WHEN e.id = 3 AND s.estado = 0 THEN 1 END) AS aire_estado_0,
                COUNT(CASE WHEN e.id = 4 AND s.estado = 1 THEN 1 END) AS tierra_estado_1,
                COUNT(CASE WHEN e.id = 4 AND s.estado = 0 THEN 1 END) AS tierra_estado_0
            FROM 
                participante p
            LEFT JOIN 
                seleccion s ON s.PARTICIPANTEid = p.id
            LEFT JOIN 
                agrupacion a ON s.AGRUPACIONGRUPOid = a.GRUPOid AND s.AGRUPACIONCUALIDADid = a.CUALIDADid
            LEFT JOIN 
                cualidad c ON a.CUALIDADid = c.id
            LEFT JOIN 
                elemento e ON c.ELEMENTOid = e.id
            WHERE 
                UPPER(CONCAT(p.nombres, ' ' , p.apellidos)) LIKE UPPER ('%'''+nombre+'''%')
            GROUP BY 
                p.id, p.nombres, p.apellidos, p.telefono, p.correo, p.fecha_registro
            ORDER BY 
                grupos_seleccionados , p.fecha_registro
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
    conexion.close()
    return result


def insertar_participante(nombres, apellidos, fecha_nacimiento, telefono, correo):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO participante (nombres, apellidos, fecha_nacimiento, telefono, correo, fecha_registro)
                VALUES (%s, %s, %s, %s, %s, NOW());
            """
            
            cursor.execute(sql, (nombres, apellidos, fecha_nacimiento, telefono, correo))
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


def obtener_elementos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql= '''
            SELECT 
                *
            FROM 
                elemento ele;
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
    conexion.close()
    return result



def eliminar_participante_id(participante_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''  delete from participante where id = '''+str(participante_id)+''' ;  '''
        # print(sql)
        cursor.execute(sql)
    conexion.commit()
    conexion.close()

