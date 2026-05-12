from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import usuario as UsuarioModel
from routes.decorators import login_required, roles_required

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/")
@roles_required("administrador")
def list():
    usuarios = UsuarioModel.get_all()
    return render_template("usuarios/list.html", usuarios=usuarios)


@usuarios_bp.route("/nuevo", methods=["GET", "POST"])
@roles_required("administrador")
def create():
    roles = UsuarioModel.get_roles()
    if request.method == "POST":
        password  = request.form.get("password", "")
        confirma  = request.form.get("confirma_password", "")
        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "warning")
        elif password != confirma:
            flash("Las contraseñas no coinciden.", "warning")
        else:
            try:
                UsuarioModel.create(
                    nombre  = request.form["nombre"].strip(),
                    email   = request.form["email"].strip().lower(),
                    password= password,
                    id_rol  = int(request.form["idRol"]),
                )
                flash("Usuario creado correctamente.", "success")
                return redirect(url_for("usuarios.list"))
            except Exception as e:
                flash(f"Error: {e}", "danger")
    return render_template("usuarios/form.html", usuario=None, roles=roles, titulo="Nuevo Usuario")


@usuarios_bp.route("/<int:id_usuario>/editar", methods=["GET", "POST"])
@roles_required("administrador")
def edit(id_usuario):
    usuario = UsuarioModel.get_by_id(id_usuario)
    roles   = UsuarioModel.get_roles()
    if not usuario:
        flash("Usuario no encontrado.", "warning")
        return redirect(url_for("usuarios.list"))

    if request.method == "POST":
        password = request.form.get("password", "").strip()
        confirma = request.form.get("confirma_password", "").strip()
        if password and len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "warning")
        elif password and password != confirma:
            flash("Las contraseñas no coinciden.", "warning")
        else:
            try:
                UsuarioModel.update(
                    id_usuario = id_usuario,
                    nombre     = request.form["nombre"].strip(),
                    email      = request.form["email"].strip().lower(),
                    id_rol     = int(request.form["idRol"]),
                    activo     = int(request.form.get("activo", 1)),
                    password   = password or None,
                )
                flash("Usuario actualizado.", "success")
                return redirect(url_for("usuarios.list"))
            except Exception as e:
                flash(f"Error: {e}", "danger")

    return render_template("usuarios/form.html", usuario=usuario, roles=roles, titulo="Editar Usuario")


@usuarios_bp.route("/<int:id_usuario>/eliminar", methods=["POST"])
@roles_required("administrador")
def delete(id_usuario):
    if id_usuario == session.get("usuario_id"):
        flash("No podés eliminar tu propio usuario.", "warning")
        return redirect(url_for("usuarios.list"))
    try:
        UsuarioModel.delete(id_usuario)
        flash("Usuario eliminado.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar: {e}", "danger")
    return redirect(url_for("usuarios.list"))
