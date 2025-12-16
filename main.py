from DAO.usuario_dao import UsuarioDAO
from DAO.reserva_dao import ReservaDAO
from DAO.paquete_dao import PaqueteDAO
import os
import sys
import SCRIPTS.setup_database as setup_db

# Intentamos importar msvcrt para los asteriscos (Solo Windows)
try:
    import msvcrt
except ImportError:
    msvcrt = None
    import getpass

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_password(mensaje="Contraseña: "):
    """Permite escribir contraseña mostrando asteriscos"""
    if msvcrt:
        print(mensaje, end='', flush=True)
        password = ""
        while True:
            char = msvcrt.getch()
            
            if char == b'\r':  # Enter
                print()
                break
            elif char == b'\x08':  # Backspace
                if password:
                    password = password[:-1]
                    # Borra el asterisco visualmente: Retrocede, Espacio, Retrocede
                    print('\b \b', end='', flush=True)
            elif char == b'\x03': # Ctrl+C para salir si se arrepiente
                print("\nCancelado.")
                sys.exit()
            else:
                # Decodificar el byte a caracter y agregarlo
                try:
                    char_decoded = char.decode('utf-8')
                    password += char_decoded
                    print('*', end='', flush=True)
                except:
                    pass # Ignorar teclas especiales
        return password
    else:
        # Fallback para Mac/Linux (no muestra asteriscos, pero oculta el texto)
        return getpass.getpass(mensaje)

def mostrar_menu_principal():
    print("\n--- ✈️  VIAJES AVENTURA  ✈️ ---")
    print("1. Iniciar Sesión")
    print("2. Registrarse (Clientes)")
    print("3. Salir")

def mostrar_menu_admin():
    print(f"\n--- 🛠️ PANEL DE ADMINISTRADOR ---")
    print("1. Agregar Nuevo Paquete")
    print("2. Eliminar Paquete")
    print("3. Ver Lista de Paquetes")
    print("4. Cerrar Sesión")

def mostrar_menu_usuario(usuario_nombre):
    print(f"\n--- 🎒 Bienvenido, {usuario_nombre} ---")
    print("1. Ver Paquetes y Reservar")
    print("2. Mi Historial de Reservas")
    print("3. Cerrar Sesión")

def main():
    # 1. Verificar e inicializar base de datos automáticamente
    print("⚙️ Verificando sistema...")
    setup_db.inicializar_base_datos()
    limpiar_pantalla()

    # 2. Instanciamos todos los DAOs
    usuario_dao = UsuarioDAO()
    reserva_dao = ReservaDAO()
    paquete_dao = PaqueteDAO() 
    
    usuario_actual = None # Almacena el DTO del usuario logueado

    while True:
        # --- ESTADO: NO LOGUEADO ---
        if not usuario_actual:
            mostrar_menu_principal()
            opcion = input("Seleccione una opción: ")

            if opcion == '1': # LOGIN
                email = input("Email: ")
                # AQUÍ USAMOS LA NUEVA FUNCIÓN CON ASTERISCOS
                password = input_password("Contraseña: ")
                
                login_result = usuario_dao.login(email, password)
                
                if login_result:
                    usuario_actual = login_result
                    print(f"✅ ¡Login exitoso! Rol: {usuario_actual.rol}")
                else:
                    print("❌ Credenciales incorrectas.")
            
            elif opcion == '2': # REGISTRO (Solo Clientes)
                nombre = input("Nombre completo: ")
                email = input("Email: ")
                # AQUÍ TAMBIÉN USAMOS LA NUEVA FUNCIÓN
                password = input_password("Contraseña: ")
                
                if usuario_dao.registrar(nombre, email, password):
                    print("✅ Usuario registrado. Ahora inicie sesión.")
                else:
                    print("❌ Error al registrar (¿El email ya existe?).")
            
            elif opcion == '3': # SALIR
                print("¡Hasta luego!")
                break
        
        # --- ESTADO: LOGUEADO ---
        else:
            if usuario_actual.rol == 'admin':
                mostrar_menu_admin()
                opcion = input(">> ")

                if opcion == '1': # Agregar Paquete
                    try:
                        nombre = input("Nombre del Paquete: ")
                        desc = input("Descripción corta: ")
                        precio = float(input("Precio: "))
                        stock = int(input("Stock inicial: "))
                        if paquete_dao.crear_paquete(nombre, desc, precio, stock):
                            print("✅ Paquete creado exitosamente.")
                    except ValueError:
                        print("❌ Error: Precio y Stock deben ser números.")

                elif opcion == '2': # Eliminar Paquete
                    try:
                        id_p = int(input("Ingrese ID del paquete a eliminar: "))
                        if paquete_dao.eliminar_paquete(id_p):
                            print("✅ Paquete eliminado.")
                        else:
                            print("❌ Error al eliminar (quizás no existe).")
                    except ValueError:
                        print("❌ Error: Ingrese un ID numérico.")

                elif opcion == '3': # Listar
                    paquetes = reserva_dao.listar_paquetes()
                    print("\n--- Inventario Actual ---")
                    print(f"{'ID':<5} {'Nombre':<25} {'Stock'}")
                    for p in paquetes:
                        print(f"{p['id']:<5} {p['nombre']:<25} {p['stock']}")

                elif opcion == '4':
                    usuario_actual = None
                    print("Sesión cerrada.")

            else:
                mostrar_menu_usuario(usuario_actual.nombre)
                opcion = input(">> ")

                if opcion == '1': # Reservar
                    paquetes = reserva_dao.listar_paquetes()
                    print("\n--- Paquetes Disponibles ---")
                    print(f"{'ID':<5} {'Nombre':<25} {'Precio':<12} {'Stock'}")
                    print("-" * 50)
                    for p in paquetes:
                        print(f"{p['id']:<5} {p['nombre']:<25} ${p['precio']:<11} {p['stock']}")
                    
                    try:
                        pid = int(input("\nIngrese ID del paquete a reservar (0 para volver): "))
                        if pid > 0:
                            paquete_selec = next((p for p in paquetes if p['id'] == pid), None)
                            if paquete_selec:
                                confirm = input(f"¿Confirmar reserva de '{paquete_selec['nombre']}' por ${paquete_selec['precio']}? (s/n): ")
                                if confirm.lower() == 's':
                                    exito = reserva_dao.crear_reserva(usuario_actual.id, pid, paquete_selec['precio'])
                                    if exito:
                                        print("🎉 ¡Reserva confirmada con éxito!")
                                    else:
                                        print("❌ No se pudo reservar (Stock agotado o error).")
                            else:
                                print("ID no válido.")
                    except ValueError:
                        print("Error: Ingrese un número válido.")

                elif opcion == '2': # Historial
                    historial = reserva_dao.obtener_historial(usuario_actual.id)
                    print("\n--- 📜 Tu Historial ---")
                    if not historial:
                        print("No tienes reservas aún.")
                    else:
                        for h in historial:
                            print(f"[{h.fecha}] {h.nombre_paquete} - ${h.total_pagado} ({h.estado})")
                
                elif opcion == '3':
                    usuario_actual = None
                    print("Sesión cerrada.")

if __name__ == "__main__":
    main()