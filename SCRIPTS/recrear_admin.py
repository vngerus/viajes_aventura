import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mysql.connector
from dotenv import load_dotenv
from UTILS.security import hash_password, verify_password

load_dotenv()

def recrear_admin():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        
        email_admin = "admin@viajes.com"
        password_admin = "admin123"
        
        print("Recreando usuario administrador...")
        
        cursor.execute("DELETE FROM usuarios WHERE email = %s", (email_admin,))
        if cursor.rowcount > 0:
            print("Admin anterior eliminado")
        
        password_hash = hash_password(password_admin)
        password_hash_str = str(password_hash).strip()
        
        if len(password_hash_str) != 96:
            print(f"Error: El hash debe tener 96 caracteres, tiene {len(password_hash_str)}")
            return
        
        cursor.execute(
            """
            INSERT INTO usuarios (nombre, email, password_hash, rol)
            VALUES (%s, %s, %s, %s)
            """,
            ("Super Admin", email_admin, password_hash_str, "admin")
        )
        
        conn.commit()
        print("Admin recreado exitosamente")
        print(f"Email: {email_admin}")
        print(f"Password: {password_admin}")
        
        cursor.execute(
            "SELECT password_hash FROM usuarios WHERE email = %s",
            (email_admin,)
        )
        stored_hash = cursor.fetchone()[0]
        
        if verify_password(stored_hash, password_admin):
            print("Verificación exitosa: El admin puede iniciar sesión")
        else:
            print("Error: La verificación falló")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"Error de MySQL: {e}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    recrear_admin()
