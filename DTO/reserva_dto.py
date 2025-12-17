from dataclasses import dataclass
from datetime import datetime

@dataclass
class ReservaDTO:
    id: int
    nombre_paquete: str
    total_pagado: float
    fecha_reserva: datetime
    estado: str
    
    # Propiedades de compatibilidad
    @property
    def id_reserva(self) -> int:
        return self.id
    
    @property
    def fecha(self) -> datetime:
        return self.fecha_reserva