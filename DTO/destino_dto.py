from dataclasses import dataclass

@dataclass
class DestinoDTO:
    id: int
    nombre: str
    descripcion: str
    actividades: str
    costo: float

