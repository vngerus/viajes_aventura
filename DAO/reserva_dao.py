from CONFIG.db import DatabaseConnection
from DTO.reserva_dto import ReservaDTO

class ReservaDAO:
    def __init__(self):
        self.db = DatabaseConnection.get_instance()

    def listar_paquetes(self):
        conn = self.db.conectar()
        if not conn: return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, precio, stock FROM paquetes WHERE stock > 0")
        return cursor.fetchall()

    def crear_reserva(self, id_usuario, id_paquete, precio):
        conn = self.db.conectar()
        if not conn: return False
        cursor = conn.cursor()

        try:
            # INICIO TRANSACCIÓN
            conn.start_transaction()

            # 1. Verificar Stock (Bloqueo para evitar overbooking)
            cursor.execute("SELECT stock FROM paquetes WHERE id = %s FOR UPDATE", (id_paquete,))
            row = cursor.fetchone()
            if not row or row[0] < 1:
                raise Exception("Stock agotado.")

            # 2. Insertar Reserva
            sql_res = "INSERT INTO reservas (usuario_id, paquete_id, total_pagado) VALUES (%s, %s, %s)"
            cursor.execute(sql_res, (id_usuario, id_paquete, precio))

            # 3. Descontar Stock
            sql_stock = "UPDATE paquetes SET stock = stock - 1 WHERE id = %s"
            cursor.execute(sql_stock, (id_paquete,))

            # CONFIRMAR CAMBIOS
            conn.commit()
            return True

        except Exception as e:
            conn.rollback() # Revertir si algo falla
            print(f"⚠️ Error en reserva: {e}")
            return False
        finally:
            cursor.close()

    def obtener_historial(self, id_usuario):
        conn = self.db.conectar()
        cursor = conn.cursor()
        sql = """
            SELECT r.id, p.nombre, r.total_pagado, r.fecha_reserva, r.estado
            FROM reservas r
            JOIN paquetes p ON r.paquete_id = p.id
            WHERE r.usuario_id = %s
            ORDER BY r.fecha_reserva DESC
        """
        cursor.execute(sql, (id_usuario,))
        rows = cursor.fetchall()
        
        # Convertir a lista de DTOs
        return [ReservaDTO(r[0], r[1], float(r[2]), r[3], r[4]) for r in rows]