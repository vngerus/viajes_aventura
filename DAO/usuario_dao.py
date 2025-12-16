from CONFIG.db import DatabaseConnection
from UTILS.security import hash_password, verify_password
from DTO.usuario_dto import UsuarioDTO

class UsuarioDAO:

    def __init__(self):
        self.db = DatabaseConnection.get_instance()

    def crear(self, nombre: str, email: str, password: str) -> None:
        conn = self.db.conectar()
        cursor = conn.cursor()

        try:
            password_hash = hash_password(password)
            sql = """
                INSERT INTO usuarios (nombre, email, password_hash)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (nombre, email, password_hash))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def obtener_por_email(self, email: str) -> UsuarioDTO | None:
        conn = self.db.conectar()
        cursor = conn.cursor()

        sql = """
            SELECT id, nombre, email, password_hash, rol
            FROM usuarios
            WHERE email = %s
        """
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        cursor.close()

        if not row:
            return None

        return UsuarioDTO(
            id=row[0],
            nombre=row[1],
            email=row[2],
            rol=row[4],
            password_hash=row[3] 
        )
