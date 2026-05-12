from flask import Flask, render_template, session
from config import Config
from models import init_app
from routes.jugadores import jugadores_bp
from routes.eventos   import eventos_bp
from routes.auth      import auth_bp
from routes.usuarios  import usuarios_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(jugadores_bp, url_prefix="/jugadores")
    app.register_blueprint(eventos_bp,   url_prefix="/eventos")
    app.register_blueprint(usuarios_bp,  url_prefix="/usuarios")

    @app.route("/")
    def index():
        if not session.get("usuario_id"):
            from flask import redirect, url_for
            return redirect(url_for("auth.login"))
        return render_template("index.html")

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
