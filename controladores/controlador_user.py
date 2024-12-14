import jwt
from controladores.bd import obtener_conexion
from clases.User import User
from datetime import datetime, timedelta

def get_user_by_username(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        query = "SELECT id, nombres_completos, usuario, clave FROM administrador where usuario = %s"
        cursor.execute(query,(username,))
        user = cursor.fetchone()
    objUser = User(user[0],user[1],user[2],user[3])
    return objUser

def generate_token(user):
    SECRET_KEY = "mi_super_secreto"
    # Declaro el tiempo en el que va a expirar el token
    time_exp = 8
    # Creo el diccionario 'payload' que luego será enviado a jwt
    payload  = dict()
    payload["user_id"] = user.id,
    payload["exp"] = datetime.utcnow() + timedelta(hours=time_exp)
    payload["iat"] = datetime.utcnow()
    # retorno el token
    return jwt.encode(payload,SECRET_KEY,algorithm="HS256")


def login(username,password):
    user = get_user_by_username(username)
    if not user:
        return {
            "error":"Usuario no encontrado"
        }
    if not user.check_password(password):
        return {
            "error":"Contraseña incorrecta"
        }
    
    token = generate_token(user)
    return {
        "message":"Login exitoso",
        "token":token,
        "user": user.to_dict()
    }

