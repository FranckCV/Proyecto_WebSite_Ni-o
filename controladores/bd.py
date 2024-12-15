import pymysql
def obtener_conexion():
    return pymysql.connect(host='localhost',
<<<<<<< HEAD
                                # port=3306,
                                port=3307,
=======
                                port=3306,
                                # port=3307,
>>>>>>> 0438a7f7533432353ff6106ce9ffd8e4277c5f6b
                                user='root',
                                password='',
                                db='bd_elementos')
