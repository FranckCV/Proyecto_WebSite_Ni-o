from werkzeug.security import generate_password_hash, check_password_hash
class User:
    def __init__(self, id, nombres_completos, usuario, clave):
        self.id = id
        self.nombres_completos = nombres_completos
        self.usuario = usuario
        self.clave = clave

    def set_password(self, raw_password):
        # Genero un hash 
        self.clave = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        # Verifico si la contraseña ingresada coincide con la 
        return check_password_hash(self.clave, raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "nombres_completos": self.nombres_completos,
            "usuario": self.usuario
        }