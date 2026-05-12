from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db


# ── Auth ─────────────────────────────────────────────────────
def get_by_email(email):
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        """SELECT u.*, r.nombre AS rol
           FROM Usuarios u JOIN Roles r ON r.idRol = u.idRol
           WHERE u.email = %s AND u.activo = 1""",
        (email,),
    )
    row = cur.fetchone()
    cur.close()
    return row


def verify_password(usuario, password):
    return check_password_hash(usuario["password_hash"], password)


# ── CRUD ──────────────────────────────────────────────────────
def get_all():
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        """SELECT u.idUsuario, u.nombre, u.email, u.activo, u.fecAlta,
                  r.nombre AS rol, r.idRol
           FROM Usuarios u JOIN Roles r ON r.idRol = u.idRol
           ORDER BY u.nombre"""
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def get_by_id(id_usuario):
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        """SELECT u.*, r.nombre AS rol
           FROM Usuarios u JOIN Roles r ON r.idRol = u.idRol
           WHERE u.idUsuario = %s""",
        (id_usuario,),
    )
    row = cur.fetchone()
    cur.close()
    return row


def get_roles():
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Roles ORDER BY idRol")
    rows = cur.fetchall()
    cur.close()
    return rows


def create(nombre, email, password, id_rol):
    db  = get_db()
    cur = db.cursor()
    cur.execute(
        """INSERT INTO Usuarios (nombre, email, password_hash, idRol)
           VALUES (%s, %s, %s, %s)""",
        (nombre, email, generate_password_hash(password), id_rol),
    )
    db.commit()
    new_id = cur.lastrowid
    cur.close()
    return new_id


def update(id_usuario, nombre, email, id_rol, activo, password=None):
    db  = get_db()
    cur = db.cursor()
    if password:
        cur.execute(
            """UPDATE Usuarios
               SET nombre=%s, email=%s, idRol=%s, activo=%s, password_hash=%s
               WHERE idUsuario=%s""",
            (nombre, email, id_rol, activo, generate_password_hash(password), id_usuario),
        )
    else:
        cur.execute(
            """UPDATE Usuarios
               SET nombre=%s, email=%s, idRol=%s, activo=%s
               WHERE idUsuario=%s""",
            (nombre, email, id_rol, activo, id_usuario),
        )
    db.commit()
    cur.close()


def delete(id_usuario):
    db  = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM Usuarios WHERE idUsuario = %s", (id_usuario,))
    db.commit()
    cur.close()
