import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    _instance = None

    def __init__(self):
        if DatabaseConnection._instance is not None:
            raise Exception("Clase Singleton: Usa DatabaseConnection.get_instance()")
        else:
            DatabaseConnection._instance = self
            self.connection = None

    @staticmethod
    def get_instance():
        if DatabaseConnection._instance is None:
            DatabaseConnection()
        return DatabaseConnection._instance

    def conectar(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASS'),
                    database=os.getenv('DB_NAME')
                )
            except mysql.connector.Error as e:
                print(f"❌ Error de Conexión: {e}")
                return None
        return self.connection

    def cerrar(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None