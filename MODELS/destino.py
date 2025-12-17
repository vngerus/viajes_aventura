class Destino:
    def __init__(self, id: int, nombre: str, descripcion: str, actividades: str, costo: float):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.actividades = actividades
        self.costo = costo
    
    def __str__(self) -> str:
        return f"{self.nombre} - ${self.costo:,.0f}"

