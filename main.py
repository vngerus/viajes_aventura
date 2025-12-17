import os
import sys
import signal
from datetime import datetime
import SCRIPTS.setup_database as setup_db

from DAO.usuario_dao import UsuarioDAO
from DAO.reserva_dao import ReservaDAO
from DAO.paquete_dao import PaqueteDAO
from DAO.destino_dao import DestinoDAO

try:
    import msvcrt
except ImportError:
    msvcrt = None
    import getpass


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def input_password(mensaje: str = "Contraseña: ") -> str:
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


def mostrar_menu_principal():
    print("\n--- ✈️  VIAJES AVENTURA  ✈️ ---")
    print("1. Iniciar Sesión")
    print("2. Registrarse")
    print("3. Salir")


def mostrar_menu_admin():
    print("\n--- 🛠️ PANEL ADMINISTRADOR ---")
    print("1. Gestión de Destinos")
    print("2. Gestión de Paquetes")
    print("3. Ver Paquetes")
    print("4. Ver Todas las Reservas")
    print("5. Cerrar Sesión")


def mostrar_menu_usuario(nombre: str):
    print(f"\n--- 🎒 Bienvenido, {nombre} ---")
    print("1. Ver Paquetes y Reservar")
    print("2. Ver Destinos y Reservar")
    print("3. Mi Historial")
    print("4. Cerrar Sesión")


def signal_handler(sig, frame):
    print("\n\n👋 Saliendo del sistema...")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    print("⚙️ Verificando sistema...")
    setup_db.inicializar_base_datos()
    limpiar_pantalla()

    usuario_dao = UsuarioDAO()
    reserva_dao = ReservaDAO()
    paquete_dao = PaqueteDAO()
    destino_dao = DestinoDAO()

    usuario_actual = None

    while True:
        if not usuario_actual:
            mostrar_menu_principal()
            opcion = input("Seleccione una opción: ").strip()

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

            elif opcion == "2":
                from UTILS.validators import validar_nombre, validar_email, validar_password
                
                nombre = input("Nombre completo: ").strip()
                email = input("Email: ").strip()
                password = input_password()

                try:
                    # Validaciones
                    es_valido, mensaje = validar_nombre(nombre)
                    if not es_valido:
                        print(f"❌ {mensaje}")
                        continue
                    
                    if not validar_email(email):
                        print("❌ Email inválido. Use el formato: usuario@dominio.com")
                        continue
                    
                    es_valido, mensaje = validar_password(password)
                    if not es_valido:
                        print(f"❌ {mensaje}")
                        continue
                    
                    usuario_dao.registrar(nombre, email, password)
                    print("✅ Usuario registrado correctamente")
                except ValueError as e:
                    print(f"❌ {e}")
                except Exception as e:
                    print(f"❌ Error al registrar usuario: {e}")

            elif opcion == "3":
                print("👋 Hasta luego")
                break

            else:
                print("Opción inválida")

        else:
            if usuario_actual.rol == "admin":
                mostrar_menu_admin()
                opcion = input(">> ").strip()

                if opcion == "1":  # Gestión de Destinos
                    print("\n--- 🗺️ GESTIÓN DE DESTINOS ---")
                    print("1. Agregar Destino")
                    print("2. Ver Destinos")
                    print("3. Modificar Destino")
                    print("4. Eliminar Destino")
                    print("5. Volver")
                    
                    sub_opcion = input(">> ").strip()
                    
                    if sub_opcion == "1":  # Crear destino
                        try:
                            nombre = input("Nombre del destino: ").strip()
                            desc = input("Descripción: ").strip()
                            actividades = input("Actividades (separadas por comas): ").strip()
                            costo = float(input("Costo: "))
                            
                            destino_id = destino_dao.crear(nombre, desc, actividades, costo)
                            print(f"✅ Destino creado con ID: {destino_id}")
                        except ValueError as e:
                            print(f"❌ {e}")
                        except Exception as e:
                            print(f"❌ Error: {e}")
                    
                    elif sub_opcion == "2":  # Listar destinos
                        destinos = destino_dao.obtener_todos()
                        print("\nID   Nombre                     Costo")
                        print("-" * 50)
                        for d in destinos:
                            print(f"{d.id:<4} {d.nombre:<25} ${d.costo:,.0f}")
                    
                    elif sub_opcion == "3":  # Modificar destino
                        try:
                            destinos = destino_dao.obtener_todos()
                            if not destinos:
                                print("❌ No hay destinos disponibles")
                                continue
                            
                            print("\nDestinos disponibles:")
                            for idx, d in enumerate(destinos, 1):
                                print(f"{idx}. {d.nombre} - ${d.costo:,.0f}")
                            
                            opcion_num = int(input("\nSeleccione el número del destino a modificar (0 para cancelar): "))
                            if opcion_num == 0:
                                continue
                            
                            if opcion_num < 1 or opcion_num > len(destinos):
                                print("❌ Opción inválida")
                                continue
                            
                            destino = destinos[opcion_num - 1]
                            
                            print(f"\nDestino actual: {destino.nombre} - ${destino.costo:,.0f}")
                            nombre = input(f"Nuevo nombre (Enter para mantener '{destino.nombre}'): ").strip() or destino.nombre
                            desc = input(f"Nueva descripción (Enter para mantener): ").strip() or destino.descripcion
                            actividades = input(f"Nuevas actividades (Enter para mantener): ").strip() or destino.actividades
                            costo_str = input(f"Nuevo costo (Enter para mantener ${destino.costo:,.0f}): ").strip()
                            costo = float(costo_str) if costo_str else destino.costo
                            
                            destino_dao.actualizar(destino.id, nombre, desc, actividades, costo)
                            print("✅ Destino actualizado")
                        except ValueError as e:
                            print(f"❌ {e}")
                        except Exception as e:
                            print(f"❌ Error: {e}")
                    
                    elif sub_opcion == "4":  # Eliminar destino
                        try:
                            destinos = destino_dao.obtener_todos()
                            if not destinos:
                                print("❌ No hay destinos disponibles")
                                continue
                            
                            print("\nDestinos disponibles:")
                            for idx, d in enumerate(destinos, 1):
                                print(f"{idx}. {d.nombre} - ${d.costo:,.0f}")
                            
                            opcion_num = int(input("\nSeleccione el número del destino a eliminar (0 para cancelar): "))
                            if opcion_num == 0:
                                continue
                            
                            if opcion_num < 1 or opcion_num > len(destinos):
                                print("❌ Opción inválida")
                                continue
                            
                            destino = destinos[opcion_num - 1]
                            confirm = input(f"¿Está seguro de eliminar '{destino.nombre}'? (s/n): ").lower()
                            
                            if confirm == "s":
                                destino_dao.eliminar(destino.id)
                                print("✅ Destino eliminado")
                        except ValueError as e:
                            print(f"❌ {e}")
                        except Exception as e:
                            print(f"❌ Error: {e}")

                elif opcion == "2":  # Gestión de Paquetes
                    print("\n--- 📦 GESTIÓN DE PAQUETES ---")
                    print("1. Crear Paquete (con destinos)")
                    print("2. Crear Paquete (precio manual)")
                    print("3. Ver Paquetes")
                    print("4. Modificar Paquete")
                    print("5. Eliminar Paquete")
                    print("6. Volver")
                    
                    sub_opcion = input(">> ").strip()
                    
                    if sub_opcion == "1":  # Crear paquete con destinos (cálculo automático)
                        try:
                            # Mostrar destinos disponibles
                            destinos = destino_dao.obtener_todos()
                            print("\nDestinos disponibles:")
                            for d in destinos:
                                print(f"  {d.id}. {d.nombre} - ${d.costo:,.0f}")
                            
                            nombre = input("\nNombre del paquete: ").strip()
                            desc = input("Descripción: ").strip()
                            stock = int(input("Stock disponible: "))
                            
                            # Seleccionar destinos
                            destinos_str = input("IDs de destinos (separados por comas, ej: 1,2,3): ").strip()
                            destino_ids = [int(x.strip()) for x in destinos_str.split(",") if x.strip()]
                            
                            if not destino_ids:
                                print("❌ Debe seleccionar al menos un destino")
                                continue
                            
                            # Validar que los destinos existan
                            for did in destino_ids:
                                if not destino_dao.obtener_por_id(did):
                                    raise ValueError(f"Destino con ID {did} no existe")
                            
                            # Crear paquete (el precio se calcula automáticamente)
                            paquete_id = paquete_dao.crear_paquete(nombre, desc, stock, destino_ids)
                            precio_calculado = destino_dao.calcular_precio_paquete(destino_ids)
                            print(f"✅ Paquete creado con ID: {paquete_id}")
                            print(f"💰 Precio calculado automáticamente: ${precio_calculado:,.0f}")
                        except ValueError as e:
                            print(f"❌ {e}")
                        except Exception as e:
                            print(f"❌ Error: {e}")
                    
                    elif sub_opcion == "2":  # Crear paquete con precio manual
                        try:
                            nombre = input("Nombre: ").strip()
                            desc = input("Descripción: ").strip()
                            precio = float(input("Precio: "))
                            stock = int(input("Stock: "))
                            
                            paquete_id = paquete_dao.crear_paquete_con_precio_manual(nombre, desc, precio, stock)
                            print(f"✅ Paquete creado con ID: {paquete_id}")
                        except ValueError as e:
                            print(f"❌ {e}")
                        except Exception as e:
                            print(f"❌ Error: {e}")
                    
                    elif sub_opcion == "3":  # Ver paquetes
                        paquetes = paquete_dao.obtener_todos()
                        print("\nID   Nombre                     Precio      Stock   Destinos")
                        print("-" * 80)
                        for p in paquetes:
                            destinos_str = ", ".join([d['nombre'] for d in p['destinos']]) if p['destinos'] else "Sin destinos"
                            print(f"{p['id']:<4} {p['nombre']:<25} ${p['precio']:<10,.0f} {p['stock']:<6} {destinos_str}")
                    
                    elif sub_opcion == "4":  # Modificar paquete
                        try:
                            paquetes = paquete_dao.obtener_todos()
                            if not paquetes:
                                print("❌ No hay paquetes disponibles")
                                continue
                            
                            print("\nPaquetes disponibles:")
                            for idx, p in enumerate(paquetes, 1):
                                destinos_str = ", ".join([d['nombre'] for d in p['destinos']]) if p['destinos'] else "Sin destinos"
                                print(f"{idx}. {p['nombre']} - ${p['precio']:,.0f} - Stock: {p['stock']} - Destinos: {destinos_str}")
                            
                            opcion_num = int(input("\nSeleccione el número del paquete a modificar (0 para cancelar): "))
                            if opcion_num == 0:
                                continue
                            
                            if opcion_num < 1 or opcion_num > len(paquetes):
                                print("❌ Opción inválida")
                                continue
                            
                            paquete = paquetes[opcion_num - 1]
                            
                            print(f"\nPaquete actual: {paquete['nombre']}")
                            print(f"Precio: ${paquete['precio']:,.0f}")
                            print(f"Stock: {paquete['stock']}")
                            if paquete['destinos']:
                                print("Destinos:", ", ".join([d['nombre'] for d in paquete['destinos']]))
                            
                            nombre = input(f"Nuevo nombre (Enter para mantener '{paquete['nombre']}'): ").strip() or paquete['nombre']
                            desc = input(f"Nueva descripción (Enter para mantener): ").strip() or paquete['descripcion']
                            precio_str = input(f"Nuevo precio (Enter para mantener ${paquete['precio']:,.0f}): ").strip()
                            precio = float(precio_str) if precio_str else paquete['precio']
                            stock_str = input(f"Nuevo stock (Enter para mantener {paquete['stock']}): ").strip()
                            stock = int(stock_str) if stock_str else paquete['stock']
                            
                            paquete_dao.actualizar_paquete(paquete['id'], nombre, desc, precio, stock)
                            print("✅ Paquete actualizado")
                        except ValueError as e:
                            print(f"❌ {e}")
                        except Exception as e:
                            print(f"❌ Error: {e}")
                    
                    elif sub_opcion == "5":  # Eliminar paquete
                        try:
                            paquetes = paquete_dao.obtener_todos()
                            if not paquetes:
                                print("❌ No hay paquetes disponibles")
                                continue
                            
                            print("\nPaquetes disponibles:")
                            for idx, p in enumerate(paquetes, 1):
                                destinos_str = ", ".join([d['nombre'] for d in p['destinos']]) if p['destinos'] else "Sin destinos"
                                print(f"{idx}. {p['nombre']} - ${p['precio']:,.0f} - Stock: {p['stock']}")
                            
                            opcion_num = int(input("\nSeleccione el número del paquete a eliminar (0 para cancelar): "))
                            if opcion_num == 0:
                                continue
                            
                            if opcion_num < 1 or opcion_num > len(paquetes):
                                print("❌ Opción inválida")
                                continue
                            
                            paquete = paquetes[opcion_num - 1]
                            confirm = input(f"¿Está seguro de eliminar '{paquete['nombre']}'? (s/n): ").lower()
                            
                            if confirm == "s":
                                paquete_dao.eliminar_paquete(paquete['id'])
                                print("✅ Paquete eliminado")
                        except ValueError as e:
                            print(f"❌ {e}")
                        except Exception as e:
                            print(f"❌ Error: {e}")

                elif opcion == "3":  # Listar paquetes
                    paquetes = reserva_dao.listar_paquetes()
                    print("\nID   Nombre                     Precio      Stock")
                    print("-" * 60)
                    for p in paquetes:
                        print(f"{p['id']:<4} {p['nombre']:<25} ${p['precio']:<10,.0f} {p['stock']}")

                elif opcion == "4":  # Ver todas las reservas
                    reservas = reserva_dao.obtener_todas_reservas()
                    print("\n--- 📊 TODAS LAS RESERVAS ---")
                    if not reservas:
                        print("No hay reservas registradas")
                    else:
                        print(f"{'ID':<4} {'Usuario':<20} {'Item':<25} {'Tipo':<10} {'Total':<12} {'Fecha':<20} {'Estado':<12}")
                        print("-" * 110)
                        for r in reservas:
                            fecha_str = r['fecha_reserva'].strftime('%Y-%m-%d %H:%M') if isinstance(r['fecha_reserva'], datetime) else str(r['fecha_reserva'])
                            print(f"{r['id']:<4} {r['usuario_nombre']:<20} {r['item_nombre']:<25} {r['tipo']:<10} ${r['total_pagado']:<11,.0f} {fecha_str:<20} {r['estado']:<12}")

                elif opcion == "5":
                    usuario_actual = None
                    print("Sesión cerrada")

                else:
                    print("Opción inválida")

            else:
                mostrar_menu_usuario(usuario_actual.nombre)
                opcion = input(">> ").strip()

                if opcion == "1":  # Ver Paquetes y Reservar
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
                            precio = float(paquete["precio"])
                            reserva_dao.crear_reserva(
                                usuario_actual.id,
                                pid,
                                precio
                            )
                            print("🎉 Reserva confirmada")

                    except ValueError as e:
                        print(f"❌ {e}")
                    except Exception as e:
                        error_msg = str(e)
                        if "Stock insuficiente" in error_msg:
                            print("❌ Stock insuficiente para este paquete")
                        elif "Connection" in error_msg or "MySQL" in error_msg:
                            print("❌ Error de conexión a la base de datos")
                        else:
                            print(f"❌ Error al crear reserva: {error_msg}")

                elif opcion == "2":  # Ver Destinos y Reservar
                    destinos = reserva_dao.listar_destinos()
                    print("\nID   Nombre                     Costo")
                    print("-" * 50)
                    for d in destinos:
                        print(f"{d['id']:<4} {d['nombre']:<25} ${d['costo']:,.0f}")

                    try:
                        did = int(input("\nID del destino (0 volver): "))
                        if did == 0:
                            continue

                        destino = next((d for d in destinos if d["id"] == did), None)
                        if not destino:
                            print("❌ ID inválido")
                            continue

                        confirm = input(
                            f"¿Confirmar '{destino['nombre']}' por ${destino['costo']:,.0f}? (s/n): "
                        ).lower()

                        if confirm == "s":
                            precio = float(destino["costo"])
                            reserva_dao.crear_reserva_destino(
                                usuario_actual.id,
                                did,
                                precio
                            )
                            print("🎉 Reserva de destino confirmada")

                    except ValueError as e:
                        print(f"❌ {e}")
                    except Exception as e:
                        error_msg = str(e)
                        if "Connection" in error_msg or "MySQL" in error_msg:
                            print("❌ Error de conexión a la base de datos")
                        else:
                            print(f"❌ Error al crear reserva: {error_msg}")

                elif opcion == "3":  # Mi Historial
                    historial = reserva_dao.obtener_historial(usuario_actual.id)
                    print("\n--- 📜 Historial ---")
                    if not historial:
                        print("Sin reservas")
                    else:
                        for r in historial:
                            fecha_str = r.fecha_reserva.strftime('%Y-%m-%d %H:%M') if isinstance(r.fecha_reserva, datetime) else str(r.fecha_reserva)
                            print(f"[{fecha_str}] {r.nombre_paquete} - ${r.total_pagado:,.0f} - {r.estado}")

                elif opcion == "4":
                    usuario_actual = None
                    print("Sesión cerrada")

                else:
                    print("Opción inválida")


if __name__ == "__main__":
    main()
