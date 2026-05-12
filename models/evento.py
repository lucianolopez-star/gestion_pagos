from models import get_db


def get_all():
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT e.*,
               u.nombre                                    AS creador,
               COUNT(ej.idJugador)                         AS cant_jugadores,
               SUM(ej.monto)                               AS recaudado,
               SUM(ej.estado = 'Pagado')                   AS pagados,
               SUM(ej.estado = 'Pendiente')                AS pendientes
        FROM Eventos e
        LEFT JOIN EventoJugadores ej ON ej.idEvento = e.idEvento
        LEFT JOIN Usuarios u         ON u.idUsuario  = e.idUsuarioCreador
        GROUP BY e.idEvento
        ORDER BY e.fecEvento DESC
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


def get_by_id(id_evento):
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT e.*, u.nombre AS creador
        FROM Eventos e
        LEFT JOIN Usuarios u ON u.idUsuario = e.idUsuarioCreador
        WHERE e.idEvento = %s
    """, (id_evento,))
    row = cur.fetchone()
    cur.close()
    return row


def get_jugadores(id_evento):
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT j.idJugador, j.ApellidoNombre, j.Alias, ej.monto, ej.estado
        FROM EventoJugadores ej
        JOIN Jugadores j ON j.idJugador = ej.idJugador
        WHERE ej.idEvento = %s
        ORDER BY j.ApellidoNombre
    """, (id_evento,))
    rows = cur.fetchall()
    cur.close()
    return rows


def create(dsc_evento, fec_evento, estado, observacion, total, jugadores,
           id_usuario_creador=None):
    db  = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
            INSERT INTO Eventos (dscEvento, fecEvento, estado, Observacion, total,
                                 idUsuarioCreador)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (dsc_evento, fec_evento, estado, observacion or None,
              total or 0, id_usuario_creador))
        new_id = cur.lastrowid
        _sync_jugadores(cur, new_id, jugadores)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cur.close()
    return new_id


def update(id_evento, dsc_evento, fec_evento, estado, observacion, total, jugadores):
    db  = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
            UPDATE Eventos
            SET dscEvento=%s, fecEvento=%s, estado=%s, Observacion=%s, total=%s
            WHERE idEvento=%s
        """, (dsc_evento, fec_evento, estado, observacion or None, total or 0, id_evento))
        cur.execute("DELETE FROM EventoJugadores WHERE idEvento = %s", (id_evento,))
        _sync_jugadores(cur, id_evento, jugadores)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cur.close()


def delete(id_evento):
    db  = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM Eventos WHERE idEvento = %s", (id_evento,))
    db.commit()
    cur.close()


def duplicate(id_evento, id_usuario_creador=None):
    db  = get_db()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM Eventos WHERE idEvento = %s", (id_evento,))
        original = cur.fetchone()
        if not original:
            raise ValueError(f"Evento {id_evento} no existe.")

        cur2 = db.cursor(dictionary=True)
        cur2.execute("SELECT idJugador, monto FROM EventoJugadores WHERE idEvento = %s",
                     (id_evento,))
        jugadores_orig = cur2.fetchall()
        cur2.close()

        cur.execute("""
            INSERT INTO Eventos (dscEvento, fecEvento, estado, Observacion, total,
                                 idUsuarioCreador)
            VALUES (%s, %s, 'Pendiente', %s, %s, %s)
        """, (f"Copia de {original['dscEvento']}", original["fecEvento"],
              original["Observacion"], original["total"], id_usuario_creador))
        nuevo_id = cur.lastrowid

        _sync_jugadores(cur, nuevo_id, [
            {"idJugador": j["idJugador"], "monto": j["monto"], "estado": "Pendiente"}
            for j in jugadores_orig
        ])
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cur.close()
    return nuevo_id


def update_pago(id_evento, id_jugador, estado_pago):
    db  = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE EventoJugadores SET estado=%s WHERE idEvento=%s AND idJugador=%s",
        (estado_pago, id_evento, id_jugador),
    )
    db.commit()
    cur.close()


def _sync_jugadores(cur, id_evento, jugadores):
    if not jugadores:
        return
    cur.executemany(
        "INSERT INTO EventoJugadores (idEvento, idJugador, monto, estado) VALUES (%s,%s,%s,%s)",
        [(id_evento, j["idJugador"], j.get("monto", 0), j.get("estado", "Pendiente"))
         for j in jugadores],
    )
