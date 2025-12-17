from CONFIG.db import DatabaseConnection
from DTO.reserva_dto import ReservaDTO

class ReservaDAO:

    def __init__(self):
        self.db = DatabaseConnection.get_instance()

    def listar_paquetes(self):
        conn = self.db.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT id, nombre, precio, stock FROM paquetes WHERE stock > 0 ORDER BY id")
        paquetes = cursor.fetchall()
        cursor.close()
        return paquetes

    def crear_reserva(self, usuario_id: int, paquete_id: int, precio: float):
        conn = self.db.conectar()
        cursor = conn.cursor()

        try:
            conn.start_transaction()

            cursor.execute(
                "SELECT stock FROM paquetes WHERE id=%s FOR UPDATE",
                (paquete_id,)
            )
            row = cursor.fetchone()

            if not row or row[0] < 1:
                raise ValueError("Stock insuficiente")

            cursor.execute(
                "INSERT INTO reservas (usuario_id, paquete_id, total_pagado) VALUES (%s,%s,%s)",
                (usuario_id, paquete_id, precio)
            )

            cursor.execute(
                "UPDATE paquetes SET stock = stock - 1 WHERE id=%s",
                (paquete_id,)
            )

            conn.commit()

        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def obtener_historial(self, usuario_id: int):
        conn = self.db.conectar()
        cursor = conn.cursor()

        sql = """
            SELECT r.id, p.nombre, r.total_pagado, r.fecha_reserva, r.estado
            FROM reservas r
            JOIN paquetes p ON r.paquete_id = p.id
            WHERE r.usuario_id = %s
            ORDER BY r.fecha_reserva DESC
        """
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        cursor.close()

        return [ReservaDTO(*r) for r in rows]
