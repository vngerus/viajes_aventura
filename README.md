# Sistema de Gestion "Viajes Aventura"

Sistema de gestion de reservas turisticas desarrollado en Python para la agencia de viajes "Viajes Aventura". El sistema permite gestionar destinos, paquetes turisticos y reservas, con autenticacion segura y persistencia en base de datos MySQL.

## Instrucciones - Configurar y Ejecutar la App

1. **Crear y activar el entorno virtual**:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

2. **Instalar dependencias**:

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

3. **Configurar variables de entorno**:

Crear archivo `.env` en la raiz del proyecto:

```env
DB_HOST=localhost
DB_USER=root
DB_PASS=tu_contraseña
DB_NAME=viajes_aventura
```

4. **Inicializar la base de datos**:

```bash
python SCRIPTS/setup_database.py
```

5. **Ejecutar la aplicacion**:

```bash
python main.py
```

### Credenciales por Defecto

- **Admin**: `admin@viajes.com` / `admin123`
- **Cliente**: Registrarse desde el menu principal

## Diagrama de Clases UML

<details>
<summary><strong>Ver Diagrama</strong></summary>

![Diagrama de Clases](docs/Diagrama_Clases_UML.png)

</details>

El diagrama muestra la arquitectura del sistema con:

- **Capa DTO**: Objetos de transferencia de datos (UsuarioDTO, DestinoDTO, ReservaDTO)
- **Capa DAO**: Objetos de acceso a datos (UsuarioDAO, DestinoDAO, PaqueteDAO, ReservaDAO)
- **Capa Services**: Logica de negocio (AuthService, ReservaService)
- **Seguridad**: Hash con PBKDF2-HMAC-SHA256
- **Relaciones**: Asociaciones entre Usuario-Reserva (1:N), Paquete-Reserva (1:N) y Paquete-Destino (N:M)

## Diagrama de Casos de Uso

<details>
<summary><strong>Ver Diagrama</strong></summary>

![Diagrama de Casos de Uso](docs/Diagrama_Caso_de_Uso.png)

</details>

## Diagrama BPMN - Proceso de Reserva

<details>
<summary><strong>Ver Diagrama</strong></summary>

![Diagrama BPMN](docs/Diagrama_BPMN.png)

</details>

## Cumplimiento de la Pauta

<details>
<summary><strong>4.1.1 Identificacion de Requerimientos</strong></summary>

### Analisis Profundo de la Problematica

- Identificacion de necesidad de gestionar destinos turisticos, paquetes y reservas
- Requisitos funcionales: CRUD de destinos, CRUD de paquetes, sistema de reservas, autenticacion
- Requisitos no funcionales: Seguridad en autenticacion, integridad de datos, validacion de stock

### Pertinencia y Relevancia de los Requerimientos

- **Must Have**: CRUD completo de destinos y paquetes, autenticacion segura, persistencia en BD
- **Should Have**: Calculo automatico de precios, validacion transaccional de stock
- **Could Have**: Historial de reservas para clientes

</details>

<details>
<summary><strong>4.1.2 Diagramas UML</strong></summary>

### Precision en la Representacion de Clases

- **Diagrama**: `docs/diagrama_clases.puml` - Diagrama completo del sistema
- **Imagen**: `docs/Diagrama_Clases_UML.png` - Visualizacion en formato PNG
- **Herramienta**: PlantUML - Estandar UML con notacion correcta

### Cumplimiento de la Notacion UML

- **Notacion correcta**: Uso de `+` para publico, `-` para privado, `__` para separadores
- **Relaciones**: Herencia, dependencias, asociaciones correctamente representadas
- **Paquetes**: Organizacion por capas con colores distintivos

### Diagrama de Casos de Uso

- **Diagrama**: `docs/diagrama_casos_uso.puml` - Casos de uso del sistema
- **Imagen**: `docs/Diagrama_Caso_de_Uso.png` - Visualizacion en formato PNG
- **Actores**: Administrador y Cliente claramente definidos

</details>

<details>
<summary><strong>4.1.3 Procesos de Negocio BPMN</strong></summary>

### Comprension de los Procesos de Negocios con BPMN

- **Diagrama**: `docs/diagrama_bpmn_reserva.puml` - Proceso de reserva de paquete
- **Imagen**: `docs/Diagrama_BPMN.png` - Visualizacion en formato PNG
- **Notacion BPMN**: Uso correcto de actividades, compuertas XOR, swimlanes y notas
- **Proceso detallado**: Validacion de stock, transaccion ACID, actualizacion de inventario

### Coherencia y Consistencia en la Representacion de Procesos

- **Alineacion con requisitos**: El proceso refleja exactamente la implementacion del codigo
- **Transacciones**: Representacion correcta de SELECT FOR UPDATE y control transaccional

</details>

<details>
<summary><strong>4.1.4 Metodologias Agiles</strong></summary>

### Comprension y Aplicacion de Roles del Equipo

- **Metodologia**: Scrum aplicado durante el desarrollo
- **Roles**: Product Owner, Scrum Master, Development Team
- **Asignacion de tareas**: Responsabilidades distribuidas por capas

### Gestion de Plazos de Entrega

- **Sprints**: Iteraciones de 1-2 semanas
- **Product Backlog**: Requerimientos priorizados (Must Have, Should Have, Could Have)
- **Sprint Backlog**: Tareas especificas por iteracion

</details>

<details>
<summary><strong>4.1.5 Implementacion Tecnica</strong></summary>

### Implementacion Efectiva de Autenticacion Segura

- **Algoritmo**: PBKDF2-HMAC-SHA256
- **Implementacion**: `UTILS/security.py` - Funciones `hash_password()` y `verify_password()`
- **Caracteristicas**: Salt aleatorio (16 bytes), 100,000 iteraciones, hash de 96 caracteres
- **Validacion segura**: `DAO/usuario_dao.py` - Metodo `login()` con verificacion de hash

### Conexion Eficiente a la Base de Datos

- **Patron Singleton**: `CONFIG/db.py` - Clase `DatabaseConnection` con instancia unica
- **Libreria**: `mysql-connector-python` para conexion a MySQL
- **Transacciones**: Uso de transacciones ACID para garantizar consistencia

### Metodos CRUD

- **Destinos**: `DAO/destino_dao.py` - CRUD completo
- **Paquetes**: `DAO/paquete_dao.py` - Gestion completa con calculo automatico de precios
- **Reservas**: `DAO/reserva_dao.py` - Creacion de reservas con validacion transaccional
- **Usuarios**: `DAO/usuario_dao.py` - Gestion de usuarios del sistema

### Manejo de Excepciones

- **Bloqueos Try-Catch**: Implementados en todos los metodos DAO
- **Validaciones**: `UTILS/validators.py` - Validacion de entradas (email, password, nombre, precio, stock)

</details>

## Patrones de Diseno Utilizados

### Singleton (DatabaseConnection)

Garantiza una unica instancia de conexion a la base de datos:

```python
from CONFIG.db import DatabaseConnection

db = DatabaseConnection.get_instance()
conn = db.conectar()
```

**Justificacion**: Evita multiples conexiones simultaneas que consumen recursos.

### DAO (Data Access Object)

Separa la logica de acceso a datos de la logica de negocio:

```python
from DAO.destino_dao import DestinoDAO

destino_dao = DestinoDAO()
destino = destino_dao.obtener_por_id(1)
```

### DTO (Data Transfer Object)

Objetos ligeros para transferir datos entre capas sin exponer la estructura interna.

## Base de Datos

### Esquema Relacional

```sql
usuarios (id, nombre, email, password_hash, rol, fecha_registro)
destinos (id, nombre, descripcion, actividades, costo, fecha_creacion)
paquetes (id, nombre, descripcion, precio, stock, fecha_creacion)
paquete_destinos (paquete_id, destino_id, orden)  -- Relacion N:M
reservas (id, usuario_id, paquete_id, fecha_reserva, total_pagado, estado)
```

### Integridad Referencial

- **Foreign Keys**: Todas las relaciones estan protegidas con claves foraneas
- **CASCADE**: Eliminar un usuario elimina sus reservas
- **RESTRICT**: No se puede eliminar un destino asociado a un paquete
- **Transacciones**: Las reservas usan transacciones para garantizar consistencia

## Funcionalidades Principales

### Para Administradores

- **Gestion de Destinos**: CRUD completo de destinos turisticos
- **Gestion de Paquetes**: Crear paquetes con calculo automatico de precios basado en destinos

### Para Clientes

- **Registro y Autenticacion**: Sistema seguro de registro y login
- **Reservas**: Ver paquetes disponibles y realizar reservas con validacion de stock
- **Historial**: Ver historial de reservas propias

## Calculo Automatico de Precios

Cuando se crea un paquete seleccionando destinos, el precio se calcula automaticamente sumando los costos de los destinos incluidos.

## Validacion de Stock

El sistema implementa validacion transaccional usando `SELECT FOR UPDATE` para prevenir overbooking y garantizar consistencia de datos.

## Tecnologias Utilizadas

- **Python 3.8+**: Lenguaje de programacion
- **MySQL**: Base de datos relacional
- **mysql-connector-python**: Conector para MySQL
- **python-dotenv**: Gestion de variables de entorno
- **hashlib**: Algoritmos de hashing (PBKDF2)
- **tabulate**: Formato de tablas en consola
- **PlantUML**: Generacion de diagramas UML

## Estructura de Archivos

```
viajes_aventura/
├── BDD/                      # Scripts de base de datos
│   └── init_db.sql           # Esquema relacional
├── CONFIG/                   # Configuracion
│   └── db.py                 # Singleton para conexion BD
├── DAO/                      # Data Access Object
│   ├── destino_dao.py
│   ├── paquete_dao.py
│   ├── reserva_dao.py
│   └── usuario_dao.py
├── DTO/                      # Data Transfer Object
│   ├── destino_dto.py
│   ├── reserva_dto.py
│   └── usuario_dto.py
├── MODELS/                   # Modelos de dominio
│   ├── destino.py
│   ├── paquete.py
│   └── usuario.py
├── SERVICES/                 # Logica de negocio
│   ├── auth_service.py
│   └── reserva_service.py
├── UTILS/                    # Utilidades
│   ├── security.py           # Hashing y seguridad
│   └── validators.py         # Validaciones
├── SCRIPTS/                  # Scripts auxiliares
│   ├── setup_database.py     # Inicializacion BD
│   └── recrear_admin.py      # Recrear usuario admin
├── docs/                     # Documentacion
│   ├── diagrama_clases.puml
│   ├── diagrama_casos_uso.puml
│   ├── diagrama_bpmn_reserva.puml
│   └── generar_diagramas.py
└── main.py                   # Punto de entrada
```

## Solucion de Problemas

### Error: "Too many connections"

- Verificar que se este usando el patron Singleton correctamente
- Revisar que las conexiones se cierren despues de usar

### Error: "Access denied for user"

- Verificar credenciales en `.env`
- Asegurar que MySQL este corriendo

### Error: "Table doesn't exist"

- Ejecutar `python SCRIPTS/setup_database.py` para inicializar la BD

### Error: "Credenciales invalidas" al iniciar sesion

- Ejecutar `python SCRIPTS/recrear_admin.py` para recrear el admin

## Generar Diagramas

Para generar los diagramas UML y BPMN:

```bash
python docs/generar_diagramas.py
```

O usar el servidor web de PlantUML: http://www.plantuml.com/plantuml/uml/

## Autores

- **Equipo de Desarrollo**: Á. S.
- **Docente**: Maria del Pilar Gallego Martinez
- **Asignatura**: Programacion Orientada a Objeto Seguro
- **Carrera**: Analista Programador
