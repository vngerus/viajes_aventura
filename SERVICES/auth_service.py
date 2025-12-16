from DAO.usuario_dao import UsuarioDAO
from UTILS.security import hash_password, verify_password

class AuthService:

    def __init__(self):
        self.usuario_dao = UsuarioDAO()

    def registrar(self, email: str, password: str):
        if self.usuario_dao.obtener_por_email(email):
            raise ValueError("El usuario ya existe")

        password_hash = hash_password(password)
        return self.usuario_dao.crear(email, password_hash)

    def login(self, email: str, password: str):
        usuario = self.usuario_dao.obtener_por_email(email)

        if not usuario:
            raise ValueError("Usuario no encontrado")

        if not verify_password(password, usuario.password_hash):
            raise ValueError("Credenciales inválidas")

        return usuario
