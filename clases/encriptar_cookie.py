import hashlib
import hmac
import base64

SECRET_KEY = b"clave_super_segura"

def generar_hash(valor):
    """
    Genera un hash basado en el valor proporcionado.
    """
    valor_bytes = str(valor).encode('utf-8')
    hash_obj = hmac.new(SECRET_KEY, valor_bytes, hashlib.sha256)
    return base64.urlsafe_b64encode(hash_obj.digest()).decode('utf-8')

def verificar_hash(valor, hash_recibido):
    """
    Verifica que el hash recibido sea válido para el valor proporcionado.
    """
    hash_calculado = generar_hash(valor)
    return hmac.compare_digest(hash_calculado, hash_recibido)