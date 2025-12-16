import mysql.connector
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

class DatabaseConnection:
    _instance = None

    def __init__(self):
        if DatabaseConnection._instance is not None:
            raise Exception("Use DatabaseConnection.get_instance()")
        self.connection = None
        DatabaseConnection._instance = self

    @staticmethod
    def get_instance():
        if DatabaseConnection._instance is None:
            DatabaseConnection()
        return DatabaseConnection._instance

    def conectar(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASS"),
                    database=os.getenv("DB_NAME"),
                    autocommit=False
                )
                logging.info("Conexión a BD establecida")
            except mysql.connector.Error as e:
                logging.error("Error de conexión BD", exc_info=True)
                raise
        return self.connection

    def cerrar(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None
            logging.info("Conexión BD cerrada")
