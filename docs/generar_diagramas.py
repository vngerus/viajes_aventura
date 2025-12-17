import os
import subprocess
import sys
import urllib.request

def descargar_plantuml_jar():
    docs_dir = os.path.dirname(__file__)
    plantuml_jar = os.path.join(docs_dir, 'plantuml.jar')
    
    if os.path.exists(plantuml_jar):
        return True, plantuml_jar
    
    # Buscar si hay algún JAR de PlantUML con otro nombre
    for file in os.listdir(docs_dir):
        if file.startswith('plantuml') and file.endswith('.jar'):
            jar_path = os.path.join(docs_dir, file)
            print(f"✅ Encontrado: {file}")
            return True, jar_path
    
    print("📥 Descargando plantuml.jar...")
    try:
        url = "https://github.com/plantuml/plantuml/releases/download/v1.2024.6/plantuml-1.2024.6.jar"
        urllib.request.urlretrieve(url, plantuml_jar)
        print(f"✅ plantuml.jar descargado exitosamente")
        return True, plantuml_jar
    except Exception as e:
        print(f"❌ Error al descargar plantuml.jar: {e}")
        return False, None

def verificar_java():
    try:
        result = subprocess.run(
            ['java', '-version'],
            capture_output=True,
            text=True
        )
        return True
    except FileNotFoundError:
        return False

def generar_imagen_png_con_jar(puml_path, png_path):
    docs_dir = os.path.dirname(__file__)
    
    success, plantuml_jar = descargar_plantuml_jar()
    if not success:
        return False, "No se pudo obtener plantuml.jar"
    
    if not verificar_java():
        return False, "Java no está instalado o no está en el PATH"
    
    try:
        # Ejecutar: java -jar plantuml.jar -tpng archivo.puml
        result = subprocess.run(
            ['java', '-jar', plantuml_jar, '-tpng', puml_path],
            capture_output=True,
            text=True,
            cwd=docs_dir
        )
        
        if result.returncode == 0:
            return True, None
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            return False, error_msg
    except FileNotFoundError:
        return False, "Java no está instalado o no está en el PATH"
    except Exception as e:
        return False, str(e)

def generar_diagrama_clases():
    contenido = """@startuml diagrama_clases

skinparam classAttributeIconSize 0
skinparam backgroundColor #FFFFFF
skinparam roundcorner 5

title Sistema de Gestión "Viajes Aventura"\nDiagrama de Clases UML

package "Capa DTO - Data Transfer Objects" #DDFFDD {
    
    class UsuarioDTO {
        +id: int
        +nombre: str
        +email: str
        +rol: str
        __
        +to_dict(): dict
    }
    
    class DestinoDTO {
        +id: int
        +nombre: str
        +descripcion: str
        +actividades: str
        +costo: float
        __
        +to_dict(): dict
    }
    
    class ReservaDTO {
        +id: int
        +nombre_paquete: str
        +total_pagado: float
        +fecha_reserva: datetime
        +estado: str
        __
        +to_dict(): dict
    }
}

package "Capa DAO - Data Access Objects" #DDDDFF {
    
    class UsuarioDAO {
        -db: DatabaseConnection
        __
        +crear(nombre, email, password): void
        +registrar(nombre, email, password): void
        +login(email, password): UsuarioDTO
        +obtener_por_email(email): UsuarioDTO
    }
    
    class DestinoDAO {
        -db: DatabaseConnection
        __
        +crear(nombre, descripcion, actividades, costo): int
        +obtener_todos(): list<DestinoDTO>
        +obtener_por_id(id): DestinoDTO
        +actualizar(dto): void
        +eliminar(id): void
    }
    
    class PaqueteDAO {
        -db: DatabaseConnection
        -destino_dao: DestinoDAO
        __
        +crear_paquete(nombre, descripcion, stock, destino_ids): int
        +crear_paquete_con_precio_manual(nombre, descripcion, precio, stock): int
        +obtener_todos(): list<dict>
        +obtener_por_id(id): dict
        +actualizar_paquete(id, nombre, descripcion, stock, destino_ids): void
        +eliminar_paquete(id): void
        +calcular_precio_desde_destinos(destino_ids): float
    }
    
    class ReservaDAO {
        -db: DatabaseConnection
        __
        +listar_paquetes(): list<dict>
        +crear_reserva(usuario_id, paquete_id, precio): void
        +obtener_historial(usuario_id): list<ReservaDTO>
    }
}

package "Conexion a Base de Datos" #FFFFDD {
    class DatabaseConnection {
        -_instance: DatabaseConnection
        -connection: Connection
        __
        +{static} get_instance(): DatabaseConnection
        +conectar(): Connection
        +cerrar(): void
    }
}

package "Capa de Servicios" #FFDDDD {
    class AuthService {
        -usuario_dao: UsuarioDAO
        __
        +registrar(nombre, email, password): void
        +login(email, password): UsuarioDTO
    }
    
    class ReservaService {
        -reserva_dao: ReservaDAO
        -paquete_dao: PaqueteDAO
        __
        +crear_reserva(usuario, paquete): void
    }
}

package "Modelos de Dominio" #DDEEFF {
    class Usuario {
        -id: int
        -nombre: str
        -email: str
        -password_hash: str
        -rol: str
        __
        +es_admin(): bool
    }
    
    class Destino {
        -id: int
        -nombre: str
        -descripcion: str
        -actividades: str
        -costo: float
    }
    
    class Paquete {
        -id: int
        -nombre: str
        -descripcion: str
        -precio: float
        -stock: int
    }
    
    class Reserva {
        -id: int
        -usuario_id: int
        -paquete_id: int
        -fecha_reserva: datetime
        -total_pagado: float
        -estado: str
    }
}

package "Configuración y Utilidades" #EEEEFF {
    class Security {
        +{static} hash_password(password): str
        +{static} verify_password(stored_hash, password): bool
    }
    
    class Validators {
        +{static} validar_nombre(nombre): tuple<bool, str>
        +{static} validar_email(email): bool
        +{static} validar_password(password): tuple<bool, str>
        +{static} validar_precio(precio): bool
        +{static} validar_stock(stock): bool
    }
}

' === RELACIONES DE DEPENDENCIA ===
UsuarioDAO ..> UsuarioDTO : retorna
DestinoDAO ..> DestinoDTO : retorna
ReservaDAO ..> ReservaDTO : retorna

' === RELACIONES DAO-DATABASE ===
UsuarioDAO --> DatabaseConnection : conecta
DestinoDAO --> DatabaseConnection : conecta
PaqueteDAO --> DatabaseConnection : conecta
ReservaDAO --> DatabaseConnection : conecta

' === RELACIONES DE SERVICIOS ===
AuthService --> UsuarioDAO : usa
ReservaService --> ReservaDAO : usa
ReservaService --> PaqueteDAO : usa

' === RELACIONES DE UTILIDADES ===
UsuarioDAO ..> Security : usa
AuthService ..> Security : usa
UsuarioDAO ..> Validators : usa
AuthService ..> Validators : usa

' === RELACIONES DE NEGOCIO ===
PaqueteDAO --> DestinoDAO : usa
Usuario "1" -- "*" Reserva : realiza
Paquete "1" -- "*" Reserva : es parte de
Paquete "*" -- "*" Destino : contiene

' === NOTAS ===
note right of DatabaseConnection
  <b>Patrón Singleton</b>
  Garantiza una única instancia
  de conexión a la base de datos
  para optimizar recursos
end note

note bottom of Security
  <b>Seguridad:</b>
  - Algoritmo: PBKDF2-HMAC-SHA256
  - Salt aleatorio: 16 bytes
  - Iteraciones: 100,000
  - Hash resultante: 96 caracteres
  (32 salt + 64 hash)
end note

note bottom of UsuarioDTO
  <b>DTO Pattern</b>
  Objeto de transferencia de datos
  sin lógica de negocio.
  Usado para comunicación entre capas
end note

note bottom of DatabaseConnection
  <b>Conexión MySQL</b>
  Base de datos: viajes_aventura
  Librería: mysql-connector-python
  Gestión de transacciones ACID
end note

@enduml"""
    
    docs_dir = os.path.dirname(__file__)
    puml_path = os.path.join(docs_dir, 'diagrama_clases.puml')
    png_path = os.path.join(docs_dir, 'diagrama_clases.png')
    
    with open(puml_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✅ Archivo .puml generado: {puml_path}")
    
    success, error = generar_imagen_png_con_jar(puml_path, png_path)
    if success:
        if os.path.exists(png_path):
            print(f"✅ Imagen PNG generada: {png_path}")
        else:
            print(f"⚠️  El comando se ejecutó pero no se generó el PNG")
    else:
        print(f"   ⚠️  Error: {error}")
        print(f"   💡 Asegúrate de tener Java instalado y plantuml.jar en docs/")
    
    return puml_path

def generar_diagrama_bpmn():
    contenido = """@startuml diagrama_bpmn_reserva

skinparam backgroundColor #FFFFFF
skinparam activity {
    BackgroundColor #E8F4F8
    BorderColor #2E86AB
    FontSize 12
}
skinparam note {
    BackgroundColor #FFF9E3
    BorderColor #F4A261
}

title Proceso de Negocio: Reserva de Paquete Turístico\nDiagrama BPMN

|#LightYellow|Cliente|
start
:Cliente selecciona paquete;
|#LightBlue|Sistema|
:Validar Stock\n(Compuerta XOR);
|#LightGray|Base de Datos|
:Consultar Stock\nSELECT stock FROM paquetes\nWHERE id = ? FOR UPDATE;
|#LightBlue|Sistema|
if (Stock > 0?) then (Sí)
    :Calcular Precio Total\nSuma de costos de destinos;
    :Crear Reserva\n(Transacción ACID);
    |#LightGray|Base de Datos|
    :Guardar Reserva\nINSERT INTO reservas\n(usuario_id, paquete_id, total_pagado);
    :Actualizar Stock\nUPDATE paquetes\nSET stock = stock - 1;
    |#LightBlue|Sistema|
    :Confirmar Transacción\nCOMMIT;
    |#LightYellow|Cliente|
    :Mostrar Comprobante\nID Reserva generado;
    stop
else (No - Stock = 0)
    |#LightBlue|Sistema|
    :Notificar Error\n"Stock insuficiente";
    |#LightYellow|Cliente|
    :Volver al menú de búsqueda;
    stop
endif

note right
    <b>Validación Transaccional</b>
    - SELECT FOR UPDATE: Bloqueo pesimista
    - Transacción ACID garantiza consistencia
    - Rollback automático en caso de error
    - Previene condiciones de carrera
end note

note left of "Consultar Stock"
    <b>Bloqueo de Fila</b>
    FOR UPDATE asegura que solo
    una transacción puede modificar
    el stock simultáneamente
end note

@enduml"""
    
    docs_dir = os.path.dirname(__file__)
    puml_path = os.path.join(docs_dir, 'diagrama_bpmn_reserva.puml')
    png_path = os.path.join(docs_dir, 'diagrama_bpmn_reserva.png')
    
    with open(puml_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✅ Archivo .puml generado: {puml_path}")
    
    success, error = generar_imagen_png_con_jar(puml_path, png_path)
    if success:
        if os.path.exists(png_path):
            print(f"✅ Imagen PNG generada: {png_path}")
        else:
            print(f"⚠️  El comando se ejecutó pero no se generó el PNG")
    else:
        print(f"   ⚠️  Error: {error}")
    
    return puml_path

def generar_diagrama_casos_uso():
    contenido = """@startuml diagrama_casos_uso

skinparam backgroundColor #FFFFFF
skinparam usecase {
    BackgroundColor #FFF9E3
    BorderColor #F4A261
}
skinparam actor {
    BackgroundColor #E8F4F8
    BorderColor #2E86AB
}

title Diagrama de Casos de Uso\nSistema de Gestión "Viajes Aventura"

actor Administrador as Admin
actor Cliente as Cliente

rectangle "Sistema Viajes Aventura" {
    usecase "Gestionar Destinos" as UC_GestionarDestinos
    usecase "Gestionar Paquetes" as UC_GestionarPaquetes
    
    usecase "Registrarse" as UC_Registrarse
    usecase "Iniciar Sesión" as UC_IniciarSesion
    usecase "Buscar Paquetes" as UC_BuscarPaquetes
    usecase "Realizar Reserva" as UC_RealizarReserva
    usecase "Ver Historial" as UC_VerHistorial
}

Admin --> UC_GestionarDestinos
Admin --> UC_GestionarPaquetes

Cliente --> UC_Registrarse
Cliente --> UC_IniciarSesion
Cliente --> UC_BuscarPaquetes
Cliente --> UC_RealizarReserva
Cliente --> UC_VerHistorial

UC_RealizarReserva ..> UC_IniciarSesion : <<include>>

note right of UC_RealizarReserva
    <b>Seguridad:</b>
    El caso de uso "Realizar Reserva"
    requiere que el cliente esté
    autenticado (include)
end note

note bottom of UC_GestionarDestinos
    <b>Funcionalidades:</b>
    - Crear destino
    - Listar destinos
    - Modificar destino
    - Eliminar destino
end note

note bottom of UC_GestionarPaquetes
    <b>Funcionalidades:</b>
    - Crear paquete
    - Asociar destinos
    - Calcular precio automático
    - Gestionar stock
end note

@enduml"""
    
    docs_dir = os.path.dirname(__file__)
    puml_path = os.path.join(docs_dir, 'diagrama_casos_uso.puml')
    png_path = os.path.join(docs_dir, 'diagrama_casos_uso.png')
    
    with open(puml_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✅ Archivo .puml generado: {puml_path}")
    
    success, error = generar_imagen_png_con_jar(puml_path, png_path)
    if success:
        if os.path.exists(png_path):
            print(f"✅ Imagen PNG generada: {png_path}")
        else:
            print(f"⚠️  El comando se ejecutó pero no se generó el PNG")
    else:
        print(f"   ⚠️  Error: {error}")
    
    return puml_path

if __name__ == "__main__":
    print("=" * 60)
    print("Generando diagramas PlantUML y sus imágenes PNG...")
    print("=" * 60)
    print()
    
    docs_dir = os.path.dirname(__file__)
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    
    try:
        print("1️⃣ Generando Diagrama de Clases...")
        generar_diagrama_clases()
        print()
        
        print("2️⃣ Generando Diagrama BPMN...")
        generar_diagrama_bpmn()
        print()
        
        print("3️⃣ Generando Diagrama de Casos de Uso...")
        generar_diagrama_casos_uso()
        print()
        
        print("=" * 60)
        print("✅ Proceso completado")
        print("=" * 60)
        print()
        print("📁 Archivos generados en: docs/")
        print("   - diagrama_clases.puml")
        print("   - diagrama_bpmn_reserva.puml")
        print("   - diagrama_casos_uso.puml")
        print()
        
        # Verificar si se generaron PNGs
        png_files = [
            os.path.join(docs_dir, 'diagrama_clases.png'),
            os.path.join(docs_dir, 'diagrama_bpmn_reserva.png'),
            os.path.join(docs_dir, 'diagrama_casos_uso.png')
        ]
        
        pngs_generados = [f for f in png_files if os.path.exists(f)]
        if pngs_generados:
            print("✅ Imágenes PNG generadas:")
            for png in pngs_generados:
                print(f"   - {os.path.basename(png)}")
        else:
            print("⚠️  No se generaron imágenes PNG")
            print("   Verifica que:")
            print("   1. Java esté instalado (java -version)")
            print("   2. plantuml.jar esté en la carpeta docs/")
            print("   3. O usa la extensión PlantUML en VS Code (Alt+D)")
        
    except Exception as e:
        print(f"\n❌ Error al generar diagramas: {e}")
        import traceback
        traceback.print_exc()
