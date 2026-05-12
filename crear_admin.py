"""
Ejecutar una sola vez para crear el usuario administrador inicial.
    python crear_admin.py
"""
from werkzeug.security import generate_password_hash
from app import create_app
from models import get_db

EMAIL    = "admin@sistema.com"
PASSWORD = "Admin1234"
NOMBRE   = "Administrador"

app = create_app()
with app.app_context():
    db  = get_db()
    cur = db.cursor()
    cur.execute("SELECT idRol FROM Roles WHERE nombre = 'administrador'")
    rol = cur.fetchone()
    if not rol:
        print("ERROR: ejecutá primero schema_usuarios.sql en MySQL.")
    else:
        hash_pw = generate_password_hash(PASSWORD)
        cur.execute(
            """INSERT INTO Usuarios (nombre, email, password_hash, idRol)
               VALUES (%s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)""",
            (NOMBRE, EMAIL, hash_pw, rol[0]),
        )
        db.commit()
        print(f"✓  Admin creado → email: {EMAIL}  /  contraseña: {PASSWORD}")
    cur.close()
