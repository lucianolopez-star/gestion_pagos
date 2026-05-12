-- =============================================================
-- schema_usuarios.sql
-- Ejecutar UNA SOLA VEZ, después de schema.sql
-- =============================================================
USE gestion_pagos;

CREATE TABLE IF NOT EXISTS Roles (
    idRol       INT AUTO_INCREMENT PRIMARY KEY,
    nombre      ENUM('administrador','delegado','usuario') NOT NULL UNIQUE,
    descripcion VARCHAR(200)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO Roles (nombre, descripcion) VALUES
('administrador', 'Acceso total al sistema'),
('delegado',      'Puede crear y modificar sus propios eventos'),
('usuario',       'Solo puede visualizar');

CREATE TABLE IF NOT EXISTS Usuarios (
    idUsuario     INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    email         VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    idRol         INT NOT NULL,
    activo        TINYINT(1)  NOT NULL DEFAULT 1,
    fecAlta       DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usr_rol FOREIGN KEY (idRol) REFERENCES Roles(idRol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Agregar columna creador a Eventos si no existe
ALTER TABLE Eventos
    ADD COLUMN IF NOT EXISTS idUsuarioCreador INT NULL,
    ADD CONSTRAINT fk_ev_creador
        FOREIGN KEY (idUsuarioCreador) REFERENCES Usuarios(idUsuario)
        ON DELETE SET NULL;
-- NOTA: después ejecutar:  python crear_admin.py
