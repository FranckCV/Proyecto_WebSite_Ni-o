import pymysql
def obtener_conexion():
    return pymysql.connect(host='localhost',    
                                port=3307,
                                user='root',
                                password='',
                                db='bd_elementos')
