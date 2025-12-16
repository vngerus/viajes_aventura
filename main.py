import os
import sys
import SCRIPTS.setup_database as setup_db

from DAO.usuario_dao import UsuarioDAO
from DAO.reserva_dao import ReservaDAO
from DAO.paquete_dao import PaqueteDAO

# ==============================
# UTILIDADES DE CONSOLA
# ==============================

try:
    import msvcrt  # Windows
except ImportError:
    msvcrt = None
    import getpass  # Linux / Mac


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def input_password(mensaje: str = "Contraseña: ") -> str:
    """
    Captura contraseña de forma segura.
    En Windows muestra asteriscos.
    En Linux/Mac oculta el texto.
    """
    if msvcrt:
        print(mensaje, end="", flush=True)
        password = ""

        while True:
            char = msvcrt.getch()

            if char == b"\r":  # ENTER
                print()
                break
            elif char == b"\x08":  # BACKSPACE
                if password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            elif char == b"\x03":  # CTRL+C
                print("\nCancelado.")
                sys.exit()
            else:
                try:
                    password += char.decode("utf-8")
                    print("*", end="", flush=True)
                except UnicodeDecodeError:
                    pass

        return password
    else:
        return getpass.getpass(mensaje)


# ==============================
# MENÚS
# ==============================

def mostrar_menu_principal():
    print("\n--- ✈️  VIAJES AVENTURA  ✈️ ---")
    print("1. Iniciar Sesión")
    print("2. Registrarse")
    print("3. Salir")


def mostrar_menu_admin():
    print("\n--- 🛠️ PANEL ADMINISTRADOR ---")
    print("1. Agregar Paquete")
    print("2. Eliminar Paquete")
    print("3. Ver Paquetes")
    print("4. Cerrar Sesión")


def mostrar_menu_usuario(nombre: str):
    print(f"\n--- 🎒 Bienvenido, {nombre} ---")
    print("1. Ver Paquetes y Reservar")
    print("2. Mi Historial")
    print("3. Cerrar Sesión")


# ==============================
# MAIN
# ==============================

def main():
    # Inicializar sistema y BD
    print("⚙️ Verificando sistema...")
    setup_db.inicializar_base_datos()
    limpiar_pantalla()

    # DAOs
    usuario_dao = UsuarioDAO()
    reserva_dao = ReservaDAO()
    paquete_dao = PaqueteDAO()

    usuario_actual = None

    while True:

        # ==============================
        # NO LOGUEADO
        # ==============================
        if not usuario_actual:
            mostrar_menu_principal()
            opcion = input("Seleccione una opción: ").strip()

            # LOGIN
            if opcion == "1":
                email = input("Email: ").strip()
                password = input_password()

                try:
                    usuario_actual = usuario_dao.login(email, password)
                    print(f"✅ Bienvenido {usuario_actual.nombre} ({usuario_actual.rol})")
                except ValueError as e:
                    print(f"❌ {e}")
                except Exception:
                    print("❌ Error interno del sistema")

            # REGISTRO
            elif opcion == "2":
                nombre = input("Nombre completo: ").strip()
                email = input("Email: ").strip()
                password = input_password()

                try:
                    usuario_dao.registrar(nombre, email, password)
                    print("✅ Usuario registrado correctamente")
                except ValueError as e:
                    print(f"❌ {e}")
                except Exception:
                    print("❌ Error al registrar usuario")

            # SALIR
            elif opcion == "3":
                print("👋 Hasta luego")
                break

            else:
                print("Opción inválida")

        # ==============================
        # LOGUEADO
        # ==============================
        else:
            # -------- ADMIN --------
            if usuario_actual.rol == "admin":
                mostrar_menu_admin()
                opcion = input(">> ").strip()

                if opcion == "1":  # Crear paquete
                    try:
                        nombre = input("Nombre: ")
                        desc = input("Descripción: ")
                        precio = float(input("Precio: "))
                        stock = int(input("Stock: "))
                        paquete_dao.crear_paquete(nombre, desc, precio, stock)
                        print("✅ Paquete creado")
                    except ValueError:
                        print("❌ Datos inválidos")
                    except Exception:
                        print("❌ Error al crear paquete")

                elif opcion == "2":  # Eliminar paquete
                    try:
                        pid = int(input("ID paquete: "))
                        paquete_dao.eliminar_paquete(pid)
                        print("✅ Paquete eliminado")
                    except Exception:
                        print("❌ Error al eliminar paquete")

                elif opcion == "3":  # Listar paquetes
                    paquetes = reserva_dao.listar_paquetes()
                    print("\nID   Nombre                     Stock")
                    print("-" * 40)
                    for p in paquetes:
                        print(f"{p['id']:<4} {p['nombre']:<25} {p['stock']}")

                elif opcion == "4":
                    usuario_actual = None
                    print("Sesión cerrada")

                else:
                    print("Opción inválida")

            # -------- CLIENTE --------
            else:
                mostrar_menu_usuario(usuario_actual.nombre)
                opcion = input(">> ").strip()

                if opcion == "1":  # Reservar
                    paquetes = reserva_dao.listar_paquetes()
                    print("\nID   Nombre                     Precio   Stock")
                    print("-" * 55)
                    for p in paquetes:
                        print(f"{p['id']:<4} {p['nombre']:<25} ${p['precio']:<8} {p['stock']}")

                    try:
                        pid = int(input("\nID del paquete (0 volver): "))
                        if pid == 0:
                            continue

                        paquete = next((p for p in paquetes if p["id"] == pid), None)
                        if not paquete:
                            print("❌ ID inválido")
                            continue

                        confirm = input(
                            f"¿Confirmar '{paquete['nombre']}' por ${paquete['precio']}? (s/n): "
                        ).lower()

                        if confirm == "s":
                            reserva_dao.crear_reserva(
                                usuario_actual.id,
                                pid,
                                paquete["precio"]
                            )
                            print("🎉 Reserva confirmada")

                    except ValueError as e:
                        print(f"❌ {e}")
                    except Exception:
                        print("❌ No se pudo completar la reserva")

                elif opcion == "2":  # Historial
                    historial = reserva_dao.obtener_historial(usuario_actual.id)
                    print("\n--- 📜 Historial ---")
                    if not historial:
                        print("Sin reservas")
                    else:
                        for r in historial:
                            print(f"[{r.fecha}] {r.nombre_paquete} - ${r.total_pagado}")

                elif opcion == "3":
                    usuario_actual = None
                    print("Sesión cerrada")

                else:
                    print("Opción inválida")


# ==============================
# ENTRY POINT
# ==============================

if __name__ == "__main__":
    main()
