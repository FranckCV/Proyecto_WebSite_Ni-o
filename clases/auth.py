import jwt
from functools import wraps
from flask import session, jsonify, redirect, url_for

def check_token():
    token = session.get('token')
    if not token:
        return redirect(url_for('error_page', message="Token is missing!"))
    try:
        SECRET_KEY = "mi_super_secreto"
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for('error_page', message="Token has expired!"))
    except jwt.InvalidTokenError:
        return redirect(url_for('error_page', message="Invalid token!"))
    return None
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        error_response = check_token()
        if error_response:
            return error_response
        return f(*args, **kwargs)
    return decorated
