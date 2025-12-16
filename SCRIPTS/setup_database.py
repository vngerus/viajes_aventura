import mysql.connector
import os
from dotenv import load_dotenv
from UTILS.security import hash_password

load_dotenv()


def inicializar_base_datos():
    print(" Inicializando sistema...")

    ruta_sql = os.path.join("BDD", "init_db.sql")

    if not os.path.exists(ruta_sql):
        print(f" ERROR CRÍTICO: No se encontró el archivo '{ruta_sql}'")
        return

    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
        cursor = conn.cursor()
        print(f" Ejecutando script: {ruta_sql}")
        with open(ruta_sql, "r", encoding="utf-8") as archivo:
            sql_script = archivo.read()
        for resultado in cursor.execute(sql_script, multi=True):
            if resultado.with_rows:
                resultado.fetchall()

        print("Base de datos y tablas verificadas")

        conn.database = os.getenv("DB_NAME")
        cursor = conn.cursor()
        crear_admin(cursor)

        conn.commit()
        print("Sistema inicializado correctamente")

    except mysql.connector.Error as err:
        print(f" Error MySQL: {err}")
        print("💡 Verifica que MySQL esté encendido y las credenciales sean correctas")

    except Exception as e:
        print(f" Error inesperado: {e}")
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals() and conn.is_connected():
            conn.close()


def crear_admin(cursor):
    email_admin = "admin@viajes.com"

    cursor.execute(
        "SELECT id FROM usuarios WHERE email = %s",
        (email_admin,)
    )

    if cursor.fetchone():
        print("Admin ya existe, se omite creación")
        return

    password_hash = hash_password("admin123")

    cursor.execute(
        """
        INSERT INTO usuarios (nombre, email, password_hash, rol)
        VALUES (%s, %s, %s, %s)
        """,
        ("Super Admin", email_admin, password_hash, "admin")
    )

    print("Usuario administrador creado")


if __name__ == "__main__":
    inicializar_base_datos()
