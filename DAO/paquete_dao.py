from CONFIG.db import DatabaseConnection

class PaqueteDAO:

    def __init__(self):
        self.db = DatabaseConnection.get_instance()

    def crear_paquete(self, nombre: str, descripcion: str, precio: float, stock: int):
        if precio <= 0 or stock < 0:
            raise ValueError("Precio o stock inválido")

        conn = self.db.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO paquetes (nombre, descripcion, precio, stock) VALUES (%s,%s,%s,%s)",
                (nombre, descripcion, precio, stock)
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def eliminar_paquete(self, paquete_id: int):
        conn = self.db.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM paquetes WHERE id=%s", (paquete_id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
