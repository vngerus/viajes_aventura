CREATE DATABASE IF NOT EXISTS viajes_aventura;
USE viajes_aventura;


CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash CHAR(64) NOT NULL,
    rol ENUM('admin', 'cliente') DEFAULT 'cliente',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS paquetes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 10
);


CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    paquete_id INT NOT NULL,
    fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_pagado DECIMAL(10, 2) NOT NULL,
    estado ENUM('Confirmada', 'Cancelada') DEFAULT 'Confirmada',
    CONSTRAINT fk_reservas_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    CONSTRAINT fk_reservas_paquete
        FOREIGN KEY (paquete_id) REFERENCES paquetes(id)
);


INSERT INTO paquetes (nombre, descripcion, precio, stock) VALUES
('Torres del Paine Full', '5 días de trekking W', 500000, 5),
('San Pedro Místico', 'Valle de la Luna y Geysers', 350000, 10),
('Carretera Austral', 'Ruta escénica en 4x4', 850000, 2);
