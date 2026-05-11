from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import jugador as JugadorModel

jugadores_bp = Blueprint("jugadores", __name__)


@jugadores_bp.route("/")
def list():
    jugadores = JugadorModel.get_all()
    return render_template("jugadores/list.html", jugadores=jugadores)


@jugadores_bp.route("/nuevo", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        try:
            JugadorModel.create(
                apellido_nombre = request.form["ApellidoNombre"].strip(),
                telefono        = request.form.get("telefono", "").strip(),
                direccion       = request.form.get("direccion", "").strip(),
                alias           = request.form.get("Alias", "").strip(),
                fec_nacimiento  = request.form.get("fecNacimiento") or None,
            )
            flash("Jugador creado correctamente.", "success")
            return redirect(url_for("jugadores.list"))
        except Exception as e:
            flash(f"Error al crear jugador: {e}", "danger")

    return render_template("jugadores/form.html", jugador=None, titulo="Nuevo Jugador")


@jugadores_bp.route("/<int:id_jugador>/editar", methods=["GET", "POST"])
def edit(id_jugador):
    jugador = JugadorModel.get_by_id(id_jugador)
    if not jugador:
        flash("Jugador no encontrado.", "warning")
        return redirect(url_for("jugadores.list"))

    if request.method == "POST":
        try:
            JugadorModel.update(
                id_jugador      = id_jugador,
                apellido_nombre = request.form["ApellidoNombre"].strip(),
                telefono        = request.form.get("telefono", "").strip(),
                direccion       = request.form.get("direccion", "").strip(),
                alias           = request.form.get("Alias", "").strip(),
                fec_nacimiento  = request.form.get("fecNacimiento") or None,
            )
            flash("Jugador actualizado.", "success")
            return redirect(url_for("jugadores.list"))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")

    return render_template("jugadores/form.html", jugador=jugador, titulo="Editar Jugador")


@jugadores_bp.route("/<int:id_jugador>")
def detail(id_jugador):
    jugador = JugadorModel.get_by_id(id_jugador)
    if not jugador:
        flash("Jugador no encontrado.", "warning")
        return redirect(url_for("jugadores.list"))
    eventos = JugadorModel.get_eventos(id_jugador)
    return render_template("jugadores/detail.html", jugador=jugador, eventos=eventos)


@jugadores_bp.route("/<int:id_jugador>/eliminar", methods=["POST"])
def delete(id_jugador):
    try:
        JugadorModel.delete(id_jugador)
        flash("Jugador eliminado.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar: {e}", "danger")
    return redirect(url_for("jugadores.list"))
