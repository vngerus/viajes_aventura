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
    
    def listar_destinos(self):
        conn = self.db.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, descripcion, actividades, costo FROM destinos ORDER BY nombre")
        destinos = cursor.fetchall()
        cursor.close()
        return destinos

    def crear_reserva(self, usuario_id: int, paquete_id: int, precio: float):
        conn = self.db.conectar()
        cursor = conn.cursor()

        try:
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

        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()
    
    def crear_reserva_destino(self, usuario_id: int, destino_id: int, precio: float):
        conn = self.db.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO reservas (usuario_id, destino_id, total_pagado) VALUES (%s,%s,%s)",
                (usuario_id, destino_id, precio)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def obtener_historial(self, usuario_id: int):
        conn = self.db.conectar()
        cursor = conn.cursor()

        sql = """
            SELECT r.id, 
                   COALESCE(p.nombre, d.nombre) as nombre,
                   r.total_pagado, 
                   r.fecha_reserva, 
                   r.estado
            FROM reservas r
            LEFT JOIN paquetes p ON r.paquete_id = p.id
            LEFT JOIN destinos d ON r.destino_id = d.id
            WHERE r.usuario_id = %s
            ORDER BY r.fecha_reserva DESC
        """
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        cursor.close()

        return [ReservaDTO(*r) for r in rows]
    
    def obtener_todas_reservas(self):
        conn = self.db.conectar()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT r.id,
                   u.nombre as usuario_nombre,
                   u.email as usuario_email,
                   COALESCE(p.nombre, d.nombre) as item_nombre,
                   CASE WHEN r.paquete_id IS NOT NULL THEN 'Paquete' ELSE 'Destino' END as tipo,
                   r.total_pagado,
                   r.fecha_reserva,
                   r.estado
            FROM reservas r
            LEFT JOIN usuarios u ON r.usuario_id = u.id
            LEFT JOIN paquetes p ON r.paquete_id = p.id
            LEFT JOIN destinos d ON r.destino_id = d.id
            ORDER BY r.fecha_reserva DESC
        """
        cursor.execute(sql)
        reservas = cursor.fetchall()
        cursor.close()

        return reservas
