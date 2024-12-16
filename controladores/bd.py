import pymysql
def obtener_conexion():
    return pymysql.connect(host='localhost',
<<<<<<< HEAD
                                port=3307,
                                # port=3306,
=======
                                # port=3306,
                                port=3307,
>>>>>>> 54a274cc77613a4420d2342927473f566e95cab1
                                user='root',
                                password='',
                                db='bd_elementos')
