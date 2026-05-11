# Estructura del Proyecto: Gestión de Pagos

```
gestion_pagos/
│
├── app.py                          # Punto de entrada principal
├── config.py                       # Configuración de BD y app
├── requirements.txt                # Dependencias Python
│
├── database/
│   └── schema.sql                  # Script de creación de tablas
│
├── models/
│   ├── __init__.py
│   ├── jugador.py                  # Modelo Jugador (CRUD)
│   └── evento.py                   # Modelo Evento + EventoJugadores (CRUD)
│
├── routes/
│   ├── __init__.py
│   ├── jugadores.py                # Rutas /jugadores
│   └── eventos.py                  # Rutas /eventos
│
├── static/
│   ├── css/
│   │   └── style.css               # Estilos globales
│   └── js/
│       └── app.js                  # JS global (selección de jugadores, etc.)
│
└── templates/
    ├── base.html                   # Layout base con navbar
    ├── index.html                  # Dashboard principal
    │
    ├── jugadores/
    │   ├── list.html               # Listado de jugadores
    │   ├── form.html               # Crear / Editar jugador
    │   └── detail.html             # Detalle de jugador
    │
    └── eventos/
        ├── list.html               # Listado de eventos
        ├── form.html               # Crear / Editar evento + selección jugadores
        └── detail.html             # Detalle de evento con jugadores y montos
```
