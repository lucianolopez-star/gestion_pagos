import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import evento as EventoModel
from models import jugador as JugadorModel

eventos_bp = Blueprint("eventos", __name__)


def _parse_jugadores_form():
    """
    Extrae del formulario la lista de jugadores seleccionados.
    Retorna: [ {idJugador, monto, estado}, ... ]
    """
    ids     = request.form.getlist("jugador_ids")
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


@eventos_bp.route("/")
def list():
    eventos = EventoModel.get_all()
    return render_template("eventos/list.html", eventos=eventos)


@eventos_bp.route("/nuevo", methods=["GET", "POST"])
def create():
    todos_jugadores = JugadorModel.get_all()

    if request.method == "POST":
        try:
            jugadores = _parse_jugadores_form()
            EventoModel.create(
                dsc_evento  = request.form["dscEvento"].strip(),
                fec_evento  = request.form["fecEvento"],
                estado      = request.form["estado"],
                observacion = request.form.get("Observacion", "").strip(),
                total       = request.form.get("total", 0),
                jugadores   = jugadores,
            )
            flash("Evento creado correctamente.", "success")
            return redirect(url_for("eventos.list"))
        except Exception as e:
            flash(f"Error al crear evento: {e}", "danger")

    return render_template(
        "eventos/form.html",
        evento=None,
        todos_jugadores=todos_jugadores,
        jugadores_evento=[],
        titulo="Nuevo Evento",
    )


@eventos_bp.route("/<int:id_evento>/editar", methods=["GET", "POST"])
def edit(id_evento):
    evento          = EventoModel.get_by_id(id_evento)
    todos_jugadores = JugadorModel.get_all()

    if not evento:
        flash("Evento no encontrado.", "warning")
        return redirect(url_for("eventos.list"))

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
    return render_template(
        "eventos/form.html",
        evento=evento,
        todos_jugadores=todos_jugadores,
        jugadores_evento=jugadores_evento,
        titulo="Editar Evento",
    )


@eventos_bp.route("/<int:id_evento>")
def detail(id_evento):
    evento = EventoModel.get_by_id(id_evento)
    if not evento:
        flash("Evento no encontrado.", "warning")
        return redirect(url_for("eventos.list"))
    jugadores = EventoModel.get_jugadores(id_evento)
    return render_template("eventos/detail.html", evento=evento, jugadores=jugadores)


@eventos_bp.route("/<int:id_evento>/duplicar", methods=["POST"])
def duplicate(id_evento):
    try:
        nuevo_id = EventoModel.duplicate(id_evento)
        flash("Evento duplicado correctamente. Podés editar los datos del nuevo evento.", "success")
        return redirect(url_for("eventos.edit", id_evento=nuevo_id))
    except Exception as e:
        flash(f"No se pudo duplicar el evento: {e}", "danger")
        return redirect(url_for("eventos.list"))


@eventos_bp.route("/<int:id_evento>/eliminar", methods=["POST"])
def delete(id_evento):
    try:
        EventoModel.delete(id_evento)
        flash("Evento eliminado.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar: {e}", "danger")
    return redirect(url_for("eventos.list"))


@eventos_bp.route("/<int:id_evento>/pago", methods=["POST"])
def update_pago(id_evento):
    """Actualiza el estado de pago de un jugador en un evento (llamada AJAX o form)."""
    id_jugador  = request.form.get("idJugador")
    estado_pago = request.form.get("estadoPago")
    try:
        EventoModel.update_pago(id_evento, id_jugador, estado_pago)
        flash("Estado de pago actualizado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("eventos.detail", id_evento=id_evento))
