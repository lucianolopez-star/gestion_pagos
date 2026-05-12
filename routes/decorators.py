from functools import wraps
from flask import session, redirect, url_for, flash, abort, request


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("usuario_id"):
            flash("Debés iniciar sesión para continuar.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return f(*args, **kwargs)
    return decorated


def roles_required(*roles):
    """Ejemplo: @roles_required('administrador', 'delegado')"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get("usuario_id"):
                flash("Debés iniciar sesión para continuar.", "warning")
                return redirect(url_for("auth.login", next=request.path))
            if session.get("usuario_rol") not in roles:
                flash("No tenés permisos para realizar esta acción.", "danger")
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator
