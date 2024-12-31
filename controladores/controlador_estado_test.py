from controladores.bd import obtener_conexion

def modificar_estado_test(booleano):
    estado = 'I'
    if booleano: estado = 'A'
    
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql= "UPDATE estado_test set estado = %s;"
        afectadas = cursor.execute(sql,(estado,))
        conexion.commit()
    conexion.close()
def obtener_estado_test():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT estado FROM estado_test limit 1")
        tupla = cursor.fetchone()
    if tupla[0] == 'A': return True
    else: return False