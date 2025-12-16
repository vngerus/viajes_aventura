from CONFIG.db import DatabaseConnection
from UTILS.security import Security
from DTO.usuario_dto import UsuarioDTO

class UsuarioDAO:
    def __init__(self):
        self.db = DatabaseConnection.get_instance()

    def registrar(self, nombre, email, password):
        conn = self.db.conectar()
        if not conn: return False
        cursor = conn.cursor()
        
        hashed_pw = Security.hash_password(password)
        
        try:
            sql = "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, email, hashed_pw))
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error al registrar: {e}")
            return False
        finally:
            cursor.close()

    def login(self, email, password):
        conn = self.db.conectar()
        if not conn: return None
        cursor = conn.cursor()
        
        sql = "SELECT id, nombre, email, password_hash, rol FROM usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        
        if row and Security.verify_password(row[3], password):
            # Retornamos DTO, no el modelo crudo (ocultamos password)
            return UsuarioDTO(id=row[0], nombre=row[1], email=row[2], rol=row[4])
        return None