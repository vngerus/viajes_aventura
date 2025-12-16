from CONFIG.db import DatabaseConnection

class PaqueteDAO:
    def __init__(self):
        self.db = DatabaseConnection.get_instance()

    def crear_paquete(self, nombre, descripcion, precio, stock):
        conn = self.db.conectar()
        if not conn: return False
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO paquetes (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, descripcion, precio, stock))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al crear paquete: {e}")
            return False
        finally:
            cursor.close()

    def eliminar_paquete(self, id_paquete):
        conn = self.db.conectar()
        if not conn: return False
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM paquetes WHERE id = %s"
            cursor.execute(sql, (id_paquete,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar: {e}")
            return False
        finally:
            cursor.close()