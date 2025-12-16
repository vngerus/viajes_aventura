from DAO.usuario_dao import UsuarioDAO
from DAO.reserva_dao import ReservaDAO
from tabulate import tabulate
import getpass
import sys
import os

# Limpiar pantalla según sistema operativo
def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    usuario_dao = UsuarioDAO()
    reserva_dao = ReservaDAO()
    usuario_actual = None # Almacena el DTO del usuario logueado

    while True:
        if not usuario_actual:
            print("\n✈️  VIAJES AVENTURA - BIENVENIDO")
            print("1. Iniciar Sesión")
            print("2. Registrarse")
            print("3. Salir")
            opcion = input(">> Opción: ")

            if opcion == '1':
                email = input("Email: ")
                password = getpass.getpass("Contraseña: ")
                usuario_actual = usuario_dao.login(email, password)
                if not usuario_actual:
                    print("❌ Credenciales inválidas.")
                else:
                    limpiar()
                    print(f"✅ ¡Hola, {usuario_actual.nombre}!")

            elif opcion == '2':
                nombre = input("Nombre: ")
                email = input("Email: ")
                pwd = getpass.getpass("Contraseña: ")
                if usuario_dao.registrar(nombre, email, pwd):
                    print("✅ Registro exitoso. Inicia sesión.")
            
            elif opcion == '3':
                sys.exit()

        else:
            # MENÚ DE CLIENTE
            print(f"\n👤 Usuario: {usuario_actual.email} | Rol: {usuario_actual.rol}")
            print("1. Ver Paquetes Disponibles")
            print("2. Mis Reservas")
            print("3. Cerrar Sesión")
            opcion = input(">> Opción: ")

            if opcion == '1':
                paquetes = reserva_dao.listar_paquetes()
                if paquetes:
                    print(tabulate(paquetes, headers="keys", tablefmt="fancy_grid"))
                    try:
                        id_sel = int(input("\nID del paquete a reservar (0 cancelar): "))
                        if id_sel != 0:
                            # Buscar paquete seleccionado en la lista local
                            paquete = next((p for p in paquetes if p['id'] == id_sel), None)
                            if paquete:
                                exito = reserva_dao.crear_reserva(usuario_actual.id, id_sel, paquete['precio'])
                                if exito: print("🎉 ¡Reserva confirmada!")
                            else:
                                print("❌ ID incorrecto.")
                    except ValueError:
                        print("❌ Ingrese un número válido.")
                else:
                    print("⚠️ No hay paquetes disponibles.")

            elif opcion == '2':
                historial = reserva_dao.obtener_historial(usuario_actual.id)
                if historial:
                    data = [[h.id_reserva, h.nombre_paquete, h.total_pagado, h.fecha, h.estado] for h in historial]
                    headers = ["ID", "Paquete", "Total", "Fecha", "Estado"]
                    print(tabulate(data, headers=headers, tablefmt="simple"))
                else:
                    print("📭 Sin historial.")

            elif opcion == '3':
                usuario_actual = None
                limpiar()
                print("🔒 Sesión cerrada.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Salida forzada.")