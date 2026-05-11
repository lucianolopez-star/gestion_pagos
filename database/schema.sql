-- =============================================================
-- schema.sql  –  Gestión de Pagos por Evento
-- =============================================================

CREATE DATABASE IF NOT EXISTS gestion_pagos
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE gestion_pagos;

-- -------------------------------------------------------------
-- Tabla: Jugadores
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Jugadores (
    idJugador       INT AUTO_INCREMENT PRIMARY KEY,
    ApellidoNombre  VARCHAR(100) NOT NULL,
    telefono        VARCHAR(20),
    direccion       VARCHAR(200),
    Alias           VARCHAR(50),
    fecNacimiento   DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------
-- Tabla: Eventos
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Eventos (
    idEvento    INT AUTO_INCREMENT PRIMARY KEY,
    dscEvento   VARCHAR(150) NOT NULL,
    fecEvento   DATE         NOT NULL,
    estado      ENUM('Pendiente','Activo','Cerrado') NOT NULL DEFAULT 'Pendiente',
    Observacion TEXT,
    total       DECIMAL(10,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------
-- Tabla: EventoJugadores  (relación N:M con monto y estado)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS EventoJugadores (
    idEvento    INT            NOT NULL,
    idJugador   INT            NOT NULL,
    monto       DECIMAL(10,2)  NOT NULL DEFAULT 0.00,
    estado      ENUM('Pendiente','Pagado','Eximido') NOT NULL DEFAULT 'Pendiente',
    PRIMARY KEY (idEvento, idJugador),
    CONSTRAINT fk_ej_evento   FOREIGN KEY (idEvento)  REFERENCES Eventos(idEvento)  ON DELETE CASCADE,
    CONSTRAINT fk_ej_jugador  FOREIGN KEY (idJugador) REFERENCES Jugadores(idJugador) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------
-- Datos de prueba
-- -------------------------------------------------------------
INSERT INTO Jugadores (ApellidoNombre, telefono, direccion, Alias, fecNacimiento) VALUES
('García, Juan',    '3411234567', 'San Martín 100', 'Juancito',  '1990-05-15'),
('López, Marcos',   '3417654321', 'Belgrano 200',   'Marky',     '1988-11-20'),
('Rodríguez, Ana',  '3419876543', 'Rivadavia 300',  'Anita',     '1995-03-08'),
('Pérez, Carlos',   '3412345678', 'Mitre 400',      'Carlitos',  '1992-07-30');

INSERT INTO Eventos (dscEvento, fecEvento, estado, Observacion, total) VALUES
('Torneo Apertura 2025', '2025-03-15', 'Cerrado', 'Primera fecha del año', 5000.00),
('Campeonato Regional',  '2025-06-20', 'Activo',  NULL,                     8000.00);

INSERT INTO EventoJugadores (idEvento, idJugador, monto, estado) VALUES
(1, 1, 1250.00, 'Pagado'),
(1, 2, 1250.00, 'Pendiente'),
(1, 3, 1250.00, 'Pagado'),
(1, 4, 1250.00, 'Eximido'),
(2, 1, 2000.00, 'Pendiente'),
(2, 3, 2000.00, 'Pendiente');
