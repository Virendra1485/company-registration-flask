from flask import Flask
from record.routes import record_route
from extenstions import db, migrate, login_manager
from commands import initialize_data


def register_blueprints(app):
    """Register Flask blueprints."""

    app.register_blueprint(record_route)
    return None


def register_extensions(app):
    """Register Flask extensions."""

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    return None


def register_commands(app):
    app.cli.add_command(initialize_data)
    return None


def create_app(config_object="settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    with app.app_context():
        register_extensions(app)
        register_blueprints(app)
        register_commands(app)
    return app
