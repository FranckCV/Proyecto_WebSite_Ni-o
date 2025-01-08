import psycopg2
from psycopg2 import sql

def obtener_conexion():
    try:
        conexion = psycopg2.connect(
            host='dpg-ctveif0gph6c73eurn40-a',
            port=5432,
            user='root',
            password='Vd3QqCAEeMSLJSxp2fLADRNoGYrPTqFZ',
            dbname='bd_elementos'
        )
        return conexion
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
