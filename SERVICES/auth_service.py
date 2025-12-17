from DAO.usuario_dao import UsuarioDAO
from DTO.usuario_dto import UsuarioDTO

class AuthService:

    def __init__(self):
        self.usuario_dao = UsuarioDAO()

    def registrar(self, nombre: str, email: str, password: str) -> None:

        return self.usuario_dao.registrar(nombre, email, password)

    def login(self, email: str, password: str) -> UsuarioDTO:
        return self.usuario_dao.login(email, password)
