CREATE DATABASE IF NOT EXISTS viajes_aventura
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE viajes_aventura;

-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash CHAR(96) NOT NULL COMMENT 'Hash PBKDF2: 32 chars salt + 64 chars hash',
    rol ENUM('admin', 'cliente') DEFAULT 'cliente',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Destinos (Requerimiento crítico: Gestión de Destinos)
CREATE TABLE IF NOT EXISTS destinos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    actividades TEXT,
    costo DECIMAL(10,2) NOT NULL CHECK (costo >= 0),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Paquetes (relacionada con destinos)
CREATE TABLE IF NOT EXISTS paquetes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    stock INT NOT NULL DEFAULT 10 CHECK (stock >= 0),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de relación muchos a muchos: Paquetes-Destinos
CREATE TABLE IF NOT EXISTS paquete_destinos (
    paquete_id INT NOT NULL,
    destino_id INT NOT NULL,
    orden INT DEFAULT 1,
    
    PRIMARY KEY (paquete_id, destino_id),
    CONSTRAINT fk_paquete_destinos_paquete
        FOREIGN KEY (paquete_id)
        REFERENCES paquetes(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_paquete_destinos_destino
        FOREIGN KEY (destino_id)
        REFERENCES destinos(id)
        ON DELETE CASCADE
);

-- Tabla de Reservas
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    paquete_id INT NOT NULL,
    fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_pagado DECIMAL(10,2) NOT NULL,
    estado ENUM('Confirmada', 'Cancelada') DEFAULT 'Confirmada',

    CONSTRAINT fk_reservas_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_reservas_paquete
        FOREIGN KEY (paquete_id)
        REFERENCES paquetes(id)
        ON DELETE RESTRICT
);

-- Datos iniciales: Destinos
INSERT INTO destinos (nombre, descripcion, actividades, costo) VALUES
('Torres del Paine', 'Parque Nacional con torres de granito', 'Trekking, Fotografía, Camping', 200000),
('Valle de la Luna', 'Desierto con formaciones lunares', 'Tour guiado, Observación astronómica', 50000),
('Geysers del Tatio', 'Campo geotérmico a 4.320 msnm', 'Baños termales, Fotografía', 80000),
('Carretera Austral', 'Ruta escénica de 1.240 km', 'Conducción 4x4, Camping, Pesca', 300000),
('Glaciar Grey', 'Glaciar en el Parque Torres del Paine', 'Navegación, Trekking sobre hielo', 150000);

-- Datos iniciales: Paquetes (con cálculo automático de precios basado en destinos)
INSERT INTO paquetes (nombre, descripcion, precio, stock) VALUES
('Torres del Paine Full', '5 días de trekking W incluyendo Torres y Glaciar Grey', 500000, 5),
('San Pedro Místico', 'Valle de la Luna y Geysers del Tatio', 130000, 10),
('Carretera Austral', 'Ruta escénica completa en 4x4', 850000, 2);
