from dataclasses import dataclass

@dataclass
class UsuarioDTO:
    id: int
    nombre: str
    email: str
    rol: str
    password_hash: str = ""  # Solo para uso interno, no se expone