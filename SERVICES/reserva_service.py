class ReservaService:

    def __init__(self, reserva_dao, paquete_dao):
        self.reserva_dao = reserva_dao
        self.paquete_dao = paquete_dao

    def crear_reserva(self, usuario, paquete):
        if paquete.stock <= 0:
            raise ValueError("No hay cupos disponibles")

        paquete.stock -= 1
        self.paquete_dao.actualizar(paquete)

        return self.reserva_dao.crear(usuario.id, paquete.id)
