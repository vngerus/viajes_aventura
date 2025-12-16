from dataclasses import dataclass

@dataclass
class UsuarioDTO:
    id: int
    nombre: str
    email: str
    rol: str