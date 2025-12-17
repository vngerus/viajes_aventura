from CONFIG.db import DatabaseConnection
from DAO.destino_dao import DestinoDAO

class PaqueteDAO:

    def __init__(self):
        self.db = DatabaseConnection.get_instance()
        self.destino_dao = DestinoDAO()

    def crear_paquete(self, nombre: str, descripcion: str, stock: int, 
                     destino_ids: list[int] = None) -> int:

        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        # Calcular precio automáticamente si hay destinos
        precio = 0.0
        if destino_ids:
            precio = self.destino_dao.calcular_precio_paquete(destino_ids)
            if precio <= 0:
                raise ValueError("El precio calculado debe ser mayor a cero")
        
        conn = self.db.conectar()
        cursor = conn.cursor()

        try:
            # Insertar paquete
            cursor.execute(
                "INSERT INTO paquetes (nombre, descripcion, precio, stock) VALUES (%s,%s,%s,%s)",
                (nombre, descripcion, precio, stock)
            )
            paquete_id = cursor.lastrowid
            
            # Asociar destinos al paquete si se proporcionaron
            if destino_ids:
                for orden, destino_id in enumerate(destino_ids, start=1):
                    cursor.execute(
                        "INSERT INTO paquete_destinos (paquete_id, destino_id, orden) VALUES (%s,%s,%s)",
                        (paquete_id, destino_id, orden)
                    )
            
            conn.commit()
            return paquete_id
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear paquete: {str(e)}")
        finally:
            cursor.close()

    def crear_paquete_con_precio_manual(self, nombre: str, descripcion: str, 
                                       precio: float, stock: int) -> int:

        if precio <= 0 or stock < 0:
            raise ValueError("Precio o stock inválido")

        conn = self.db.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO paquetes (nombre, descripcion, precio, stock) VALUES (%s,%s,%s,%s)",
                (nombre, descripcion, precio, stock)
            )
            paquete_id = cursor.lastrowid
            conn.commit()
            return paquete_id
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear paquete: {str(e)}")
        finally:
            cursor.close()

    def obtener_todos(self) -> list[dict]:

        conn = self.db.conectar()
        cursor = conn.cursor(dictionary=True)
        
        sql = """
            SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock
            FROM paquetes p
            ORDER BY p.nombre
        """
        cursor.execute(sql)
        paquetes = cursor.fetchall()
        
        # Obtener destinos para cada paquete
        for paquete in paquetes:
            cursor.execute(
                """
                SELECT d.id, d.nombre, d.costo
                FROM destinos d
                JOIN paquete_destinos pd ON d.id = pd.destino_id
                WHERE pd.paquete_id = %s
                ORDER BY pd.orden
                """,
                (paquete['id'],)
            )
            paquete['destinos'] = cursor.fetchall()
        
        cursor.close()
        return paquetes

    def eliminar_paquete(self, paquete_id: int) -> None:
        conn = self.db.conectar()
        cursor = conn.cursor()

        try:
            # Verificar si hay reservas asociadas
            cursor.execute(
                "SELECT COUNT(*) FROM reservas WHERE paquete_id = %s",
                (paquete_id,)
            )
            if cursor.fetchone()[0] > 0:
                raise ValueError("No se puede eliminar: el paquete tiene reservas asociadas")
            
            cursor.execute("DELETE FROM paquetes WHERE id=%s", (paquete_id,))
            
            if cursor.rowcount == 0:
                raise ValueError("Paquete no encontrado")
            
            conn.commit()
        except ValueError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar paquete: {str(e)}")
        finally:
            cursor.close()

    def actualizar_precio_desde_destinos(self, paquete_id: int) -> float:
        conn = self.db.conectar()
        cursor = conn.cursor()
        
        try:
            # Obtener destinos del paquete
            cursor.execute(
                """
                SELECT destino_id
                FROM paquete_destinos
                WHERE paquete_id = %s
                ORDER BY orden
                """,
                (paquete_id,)
            )
            destino_ids = [row[0] for row in cursor.fetchall()]
            
            if not destino_ids:
                raise ValueError("El paquete no tiene destinos asociados")
            
            # Calcular nuevo precio
            nuevo_precio = self.destino_dao.calcular_precio_paquete(destino_ids)
            
            # Actualizar precio en la BD
            cursor.execute(
                "UPDATE paquetes SET precio = %s WHERE id = %s",
                (nuevo_precio, paquete_id)
            )
            
            if cursor.rowcount == 0:
                raise ValueError("Paquete no encontrado")
            
            conn.commit()
            return nuevo_precio
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar precio: {str(e)}")
        finally:
            cursor.close()
