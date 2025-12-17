from CONFIG.db import DatabaseConnection
from DTO.destino_dto import DestinoDTO

class DestinoDAO:

    def __init__(self):
        self.db = DatabaseConnection.get_instance()

    def crear(self, nombre: str, descripcion: str, actividades: str, costo: float) -> int:
        if costo < 0:
            raise ValueError("El costo no puede ser negativo")
        
        conn = self.db.conectar()
        cursor = conn.cursor()
        
        try:
            sql = """
                INSERT INTO destinos (nombre, descripcion, actividades, costo)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, descripcion, actividades, costo))
            conn.commit()
            destino_id = cursor.lastrowid
            return destino_id
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear destino: {str(e)}")
        finally:
            cursor.close()

    def obtener_todos(self) -> list[DestinoDTO]:
        conn = self.db.conectar()
        cursor = conn.cursor()
        
        sql = """
            SELECT id, nombre, descripcion, actividades, costo
            FROM destinos
            ORDER BY nombre
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        
        return [DestinoDTO(*row) for row in rows]

    def obtener_por_id(self, destino_id: int) -> DestinoDTO | None:
        conn = self.db.conectar()
        cursor = conn.cursor()
        
        sql = """
            SELECT id, nombre, descripcion, actividades, costo
            FROM destinos
            WHERE id = %s
        """
        cursor.execute(sql, (destino_id,))
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            return None
        
        return DestinoDTO(*row)

    def actualizar(self, destino_id: int, nombre: str, descripcion: str, 
                   actividades: str, costo: float) -> None:

        if costo < 0:
            raise ValueError("El costo no puede ser negativo")
        
        conn = self.db.conectar()
        cursor = conn.cursor()
        
        try:
            sql = """
                UPDATE destinos
                SET nombre = %s, descripcion = %s, actividades = %s, costo = %s
                WHERE id = %s
            """
            cursor.execute(sql, (nombre, descripcion, actividades, costo, destino_id))
            
            if cursor.rowcount == 0:
                raise ValueError("Destino no encontrado")
            
            conn.commit()
        except ValueError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar destino: {str(e)}")
        finally:
            cursor.close()

    def eliminar(self, destino_id: int) -> None:
        conn = self.db.conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM paquete_destinos WHERE destino_id = %s",
                (destino_id,)
            )
            if cursor.fetchone()[0] > 0:
                raise ValueError("No se puede eliminar: el destino está asociado a un paquete")
            
            cursor.execute("DELETE FROM destinos WHERE id = %s", (destino_id,))
            
            if cursor.rowcount == 0:
                raise ValueError("Destino no encontrado")
            
            conn.commit()
        except ValueError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar destino: {str(e)}")
        finally:
            cursor.close()

    def calcular_precio_paquete(self, destino_ids: list[int]) -> float:
        if not destino_ids:
            return 0.0
        
        conn = self.db.conectar()
        cursor = conn.cursor()
        
        # Crear placeholders para la consulta IN
        placeholders = ','.join(['%s'] * len(destino_ids))
        sql = f"""
            SELECT SUM(costo) as total
            FROM destinos
            WHERE id IN ({placeholders})
        """
        cursor.execute(sql, tuple(destino_ids))
        row = cursor.fetchone()
        cursor.close()
        
        return float(row[0]) if row[0] else 0.0

