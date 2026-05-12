from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models import evento as EventoModel
from models import jugador as JugadorModel
from routes.decorators import login_required, roles_required

eventos_bp = Blueprint("eventos", __name__)


def _parse_jugadores_form():
    ids = request.form.getlist("jugador_ids")
    jugadores = []
    for id_j in ids:
        monto  = request.form.get(f"monto_{id_j}", 0)
        estado = request.form.get(f"estado_{id_j}", "Pendiente")
        jugadores.append({
            "idJugador": int(id_j),
            "monto":     float(monto) if monto else 0,
            "estado":    estado,
        })
    return jugadores


def _puede_modificar(evento):
    """True si el usuario en sesión puede editar/eliminar/duplicar este evento."""
    rol = session.get("usuario_rol")
    if rol == "administrador":
        return True
    if rol == "delegado" and evento.get("idUsuarioCreador") == session.get("usuario_id"):
        return True
    return False


# ── Listado ───────────────────────────────────────────────────
@eventos_bp.route("/")
@login_required
def list():
    eventos = EventoModel.get_all()
    return render_template("eventos/list.html", eventos=eventos,
                           puede_modificar=_puede_modificar)


# ── Crear ─────────────────────────────────────────────────────
@eventos_bp.route("/nuevo", methods=["GET", "POST"])
@roles_required("administrador", "delegado")
def create():
    todos_jugadores = JugadorModel.get_all()

    if request.method == "POST":
        try:
            jugadores = _parse_jugadores_form()
            EventoModel.create(
                dsc_evento        = request.form["dscEvento"].strip(),
                fec_evento        = request.form["fecEvento"],
                estado            = request.form["estado"],
                observacion       = request.form.get("Observacion", "").strip(),
                total             = request.form.get("total", 0),
                jugadores         = jugadores,
                id_usuario_creador= session["usuario_id"],
            )
            flash("Evento creado correctamente.", "success")
            return redirect(url_for("eventos.list"))
        except Exception as e:
            flash(f"Error al crear evento: {e}", "danger")

    return render_template("eventos/form.html", evento=None,
                           todos_jugadores=todos_jugadores,
                           jugadores_evento=[], titulo="Nuevo Evento")


# ── Editar ────────────────────────────────────────────────────
@eventos_bp.route("/<int:id_evento>/editar", methods=["GET", "POST"])
@login_required
def edit(id_evento):
    evento = EventoModel.get_by_id(id_evento)
    if not evento:
        flash("Evento no encontrado.", "warning")
        return redirect(url_for("eventos.list"))

    if not _puede_modificar(evento):
        flash("No tenés permisos para editar este evento.", "danger")
        return redirect(url_for("eventos.detail", id_evento=id_evento))

    todos_jugadores = JugadorModel.get_all()

    if request.method == "POST":
        try:
            jugadores = _parse_jugadores_form()
            EventoModel.update(
                id_evento   = id_evento,
                dsc_evento  = request.form["dscEvento"].strip(),
                fec_evento  = request.form["fecEvento"],
                estado      = request.form["estado"],
                observacion = request.form.get("Observacion", "").strip(),
                total       = request.form.get("total", 0),
                jugadores   = jugadores,
            )
            flash("Evento actualizado.", "success")
            return redirect(url_for("eventos.list"))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")

    jugadores_evento = EventoModel.get_jugadores(id_evento)
    return render_template("eventos/form.html", evento=evento,
                           todos_jugadores=todos_jugadores,
                           jugadores_evento=jugadores_evento,
                           titulo="Editar Evento")


# ── Detalle ───────────────────────────────────────────────────
@eventos_bp.route("/<int:id_evento>")
@login_required
def detail(id_evento):
    evento = EventoModel.get_by_id(id_evento)
    if not evento:
        flash("Evento no encontrado.", "warning")
        return redirect(url_for("eventos.list"))
    jugadores = EventoModel.get_jugadores(id_evento)
    return render_template("eventos/detail.html", evento=evento,
                           jugadores=jugadores,
                           puede_modificar=_puede_modificar(evento))


# ── Duplicar ──────────────────────────────────────────────────
@eventos_bp.route("/<int:id_evento>/duplicar", methods=["POST"])
@roles_required("administrador", "delegado")
def duplicate(id_evento):
    try:
        nuevo_id = EventoModel.duplicate(id_evento,
                                         id_usuario_creador=session["usuario_id"])
        flash("Evento duplicado. Podés editar los datos del nuevo evento.", "success")
        return redirect(url_for("eventos.edit", id_evento=nuevo_id))
    except Exception as e:
        flash(f"No se pudo duplicar: {e}", "danger")
        return redirect(url_for("eventos.list"))


# ── Eliminar ──────────────────────────────────────────────────
@eventos_bp.route("/<int:id_evento>/eliminar", methods=["POST"])
@login_required
def delete(id_evento):
    evento = EventoModel.get_by_id(id_evento)
    if not evento:
        flash("Evento no encontrado.", "warning")
        return redirect(url_for("eventos.list"))
    if not _puede_modificar(evento):
        flash("No tenés permisos para eliminar este evento.", "danger")
        return redirect(url_for("eventos.list"))
    try:
        EventoModel.delete(id_evento)
        flash("Evento eliminado.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar: {e}", "danger")
    return redirect(url_for("eventos.list"))


# ── Estado de pago ────────────────────────────────────────────
@eventos_bp.route("/<int:id_evento>/pago", methods=["POST"])
@roles_required("administrador", "delegado")
def update_pago(id_evento):
    evento = EventoModel.get_by_id(id_evento)
    if not evento or not _puede_modificar(evento):
        flash("No tenés permisos para modificar pagos de este evento.", "danger")
        return redirect(url_for("eventos.detail", id_evento=id_evento))
    id_jugador  = request.form.get("idJugador")
    estado_pago = request.form.get("estadoPago")
    try:
        EventoModel.update_pago(id_evento, id_jugador, estado_pago)
        flash("Estado de pago actualizado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("eventos.detail", id_evento=id_evento))
