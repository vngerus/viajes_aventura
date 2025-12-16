import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def inicializar_base_datos():
    print("🔄 Conectando a MySQL para inicializar el sistema...")

    ruta_sql = os.path.join("BDD", "init_db.sql")

    if not os.path.exists(ruta_sql):
        print(f"❌ ERROR CRÍTICO: No se encontró el archivo '{ruta_sql}'")
        return

    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
        )
        cursor = conn.cursor()

        print(f"📂 Leyendo archivo: {ruta_sql}")
        with open(ruta_sql, "r", encoding="utf-8") as archivo:
            sql_script = archivo.read()

        print("⚡ Ejecutando comandos SQL...")
        iterador = cursor.execute(sql_script, multi=True)

        for resultado in iterador:
            if resultado.with_rows:
                resultado.fetchall()
        
        print("\n✅ ¡ÉXITO! Base de datos 'viajes_aventura' creada y poblada correctamente.")
        print("✅ Usuario Administrador creado.")

    except mysql.connector.Error as err:
        print(f"\n❌ Error de MySQL: {err}")
        print("💡 Pista: Verifica que XAMPP esté encendido (Apache y MySQL en verde).")
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn.is_connected(): conn.close()

if __name__ == "__main__":
    inicializar_base_datos()