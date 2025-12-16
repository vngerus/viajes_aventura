class Usuario:
    def __init__(self, id: int, email: str, password_hash: str, rol: str = "cliente"):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.rol = rol

    def es_admin(self) -> bool:
        return self.rol == "admin"