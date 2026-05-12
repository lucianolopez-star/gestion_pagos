from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import usuario as UsuarioModel
from routes.decorators import login_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("usuario_id"):
        return redirect(url_for("index"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        usuario  = UsuarioModel.get_by_email(email)

        if usuario and UsuarioModel.verify_password(usuario, password):
            session["usuario_id"]  = usuario["idUsuario"]
            session["usuario_nombre"] = usuario["nombre"]
            session["usuario_rol"] = usuario["rol"]
            flash(f"Bienvenido, {usuario['nombre']}.", "success")
            return redirect(request.args.get("next") or url_for("index"))

        flash("Email o contraseña incorrectos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    """El usuario puede cambiar su propia contraseña."""
    if request.method == "POST":
        nueva = request.form.get("nueva_password", "")
        confirma = request.form.get("confirma_password", "")
        if len(nueva) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "warning")
        elif nueva != confirma:
            flash("Las contraseñas no coinciden.", "warning")
        else:
            UsuarioModel.update(
                id_usuario = session["usuario_id"],
                nombre     = session["usuario_nombre"],
                email      = UsuarioModel.get_by_id(session["usuario_id"])["email"],
                id_rol     = UsuarioModel.get_by_id(session["usuario_id"])["idRol"],
                activo     = 1,
                password   = nueva,
            )
            flash("Contraseña actualizada correctamente.", "success")
    return render_template("auth/perfil.html")
