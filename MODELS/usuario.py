class Usuario:
    def __init__(self, id, nombre, email, password_hash, rol='cliente'):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash
        self.rol = rol