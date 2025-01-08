import pymysql
def obtener_conexion():
    return pymysql.connect(host='dpg-ctveif0gph6c73eurn40-a',    
                                port=5432,
                                # port=3307,
                                user='root',
                                password='Vd3QqCAEeMSLJSxp2fLADRNoGYrPTqFZ',
                                db='bd_elementos')
