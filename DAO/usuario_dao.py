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
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                raise ValueError("El email ya está registrado")
            
            password_hash = hash_password(password)
            sql = """
                INSERT INTO usuarios (nombre, email, password_hash)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (nombre, email, password_hash))
            conn.commit()
        except ValueError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear usuario: {str(e)}")
        finally:
            cursor.close()

    def registrar(self, nombre: str, email: str, password: str) -> None:
        return self.crear(nombre, email, password)

    def login(self, email: str, password: str) -> UsuarioDTO:
        usuario = self.obtener_por_email(email)
        
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        if not usuario.password_hash or len(usuario.password_hash) < 64:
            raise ValueError("Hash de contraseña inválido")
        
        if not verify_password(usuario.password_hash, password):
            raise ValueError("Credenciales inválidas")
        
        return UsuarioDTO(
            id=usuario.id,
            nombre=usuario.nombre,
            email=usuario.email,
            rol=usuario.rol,
            password_hash=""
        )

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

        password_hash = str(row[3]).strip() if row[3] else ""
        
        return UsuarioDTO(
            id=row[0],
            nombre=row[1],
            email=row[2],
            password_hash=password_hash,
            rol=row[4]
        )
