from models import get_db


# ── Listar todos ─────────────────────────────────────────────
def get_all():
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Jugadores ORDER BY ApellidoNombre")
    rows = cur.fetchall()
    cur.close()
    return rows


# ── Obtener uno por ID ───────────────────────────────────────
def get_by_id(id_jugador):
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Jugadores WHERE idJugador = %s", (id_jugador,))
    row = cur.fetchone()
    cur.close()
    return row


# ── Crear ────────────────────────────────────────────────────
def create(apellido_nombre, telefono, direccion, alias, fec_nacimiento):
    db  = get_db()
    cur = db.cursor()
    cur.execute(
        """INSERT INTO Jugadores (ApellidoNombre, telefono, direccion, Alias, fecNacimiento)
           VALUES (%s, %s, %s, %s, %s)""",
        (apellido_nombre, telefono or None, direccion or None,
         alias or None, fec_nacimiento or None),
    )
    db.commit()
    new_id = cur.lastrowid
    cur.close()
    return new_id


# ── Actualizar ───────────────────────────────────────────────
def update(id_jugador, apellido_nombre, telefono, direccion, alias, fec_nacimiento):
    db  = get_db()
    cur = db.cursor()
    cur.execute(
        """UPDATE Jugadores
           SET ApellidoNombre=%s, telefono=%s, direccion=%s, Alias=%s, fecNacimiento=%s
           WHERE idJugador=%s""",
        (apellido_nombre, telefono or None, direccion or None,
         alias or None, fec_nacimiento or None, id_jugador),
    )
    db.commit()
    cur.close()


# ── Eliminar ─────────────────────────────────────────────────
def delete(id_jugador):
    db  = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM Jugadores WHERE idJugador = %s", (id_jugador,))
    db.commit()
    cur.close()


# ── Eventos en los que participó un jugador ──────────────────
def get_eventos(id_jugador):
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        """SELECT e.idEvento, e.dscEvento, e.fecEvento, e.estado AS estadoEvento,
                  ej.monto, ej.estado AS estadoPago
           FROM EventoJugadores ej
           JOIN Eventos e ON e.idEvento = ej.idEvento
           WHERE ej.idJugador = %s
           ORDER BY e.fecEvento DESC""",
        (id_jugador,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows
