from flask import Flask, render_template
from config import Config
from routes.jugadores import jugadores_bp
from routes.eventos import eventos_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registrar blueprints
    app.register_blueprint(jugadores_bp, url_prefix="/jugadores")
    app.register_blueprint(eventos_bp,   url_prefix="/eventos")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
