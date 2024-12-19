import pymysql
def obtener_conexion():
    return pymysql.connect(host='localhost',
                                port=3306,
<<<<<<< HEAD
                                # port=3306,

=======
                                # port=3307,
>>>>>>> a4894b0f1b5c4defc0ed6dde960bb35cd5947ad9
                                user='root',
                                password='',
                                db='bd_elementos')
