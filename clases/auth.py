import jwt
from functools import wraps
from flask import session, jsonify

def check_token():
    token = session.get('token')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 403
    try:
        SECRET_KEY = "mi_super_secreto"
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 403
    return None
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        error_response = check_token()
        if error_response:
            return error_response
        return f(*args, **kwargs)
    return decorated
