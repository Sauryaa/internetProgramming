from pathlib import Path

from flask import Flask, redirect, url_for

from .models import Student, db
from .services import (
    DEFAULT_CAST_PATH,
    get_active_production,
    import_students_from_csv,
)
from .blueprints.edit import edit_bp
from .blueprints.view import view_bp


def create_app(test_config=None):
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    base_dir = Path(__file__).resolve().parent
    database_path = base_dir / "musical.db"
    app.config.from_mapping(
        SECRET_KEY="development-key",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{database_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        get_active_production()
        if Student.query.count() == 0 and DEFAULT_CAST_PATH.exists():
            import_students_from_csv(DEFAULT_CAST_PATH)

    app.register_blueprint(edit_bp, url_prefix="/edit")
    app.register_blueprint(view_bp, url_prefix="/view")

    @app.route("/")
    def index():
        return redirect(url_for("view.program"))

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
