import jwt
from controladores.bd import obtener_conexion
from clases.User import User
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def get_user_by_username(username):
    conexion = obtener_conexion()
    objUser = None
    with conexion.cursor() as cursor:
        query = "SELECT id, nombres_completos, usuario, clave FROM administrador where usuario = %s"
        cursor.execute(query,(username,))
        user = cursor.fetchone()
    if user:
        objUser = User(user[0],user[1],user[2],user[3])
    print(objUser)
    return objUser

def register_user(nombres_completos, usuario, clave):
    conexion = obtener_conexion()
    hashed_password = generate_password_hash(clave)
    with conexion.cursor() as cursor:
        query = """
        INSERT INTO administrador (nombres_completos, usuario, clave)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (nombres_completos, usuario, hashed_password))
    conexion.commit()
    conexion.close()
    return {"message": "Usuario registrado exitosamente"}

def generate_token(user):
    SECRET_KEY = "mi_super_secreto"
    # Declaro el tiempo en el que va a expirar el token
    time_exp = 8
    # Creo el diccionario 'payload' que luego será enviado a jwt
    payload  = dict()
    payload["user_id"] = user.id
    payload["exp"] = datetime.utcnow() + timedelta(hours=time_exp)
    payload["iat"] = datetime.utcnow()
    # retorno el token
    return jwt.encode(payload,SECRET_KEY,algorithm="HS256")


def login(username,password):
    user = get_user_by_username(username)
    print(user)
    if not user or not user.check_password(password) :
        return {
            "message":"error",
            "data":{}
        }
    
    token = generate_token(user)
    return {
        "message":"success",
        "data":{
            "token":token,
            "user": user.to_dict()
        }
    }

