from dataclasses import dataclass
from datetime import datetime

@dataclass
class ReservaDTO:
    id_reserva: int
    nombre_paquete: str
    total_pagado: float
    fecha: datetime
    estado: str