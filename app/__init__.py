"""Application factory for the Flask CRUD demo."""
from __future__ import annotations

from flask import Flask

from .config import get_config
from .extensions import db, migrate
from .resources.api import api_blueprint
from .resources.health import health_blueprint


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application."""

    app = Flask(__name__)
    app_config = get_config(config_name)
    app.config.from_object(app_config)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""

    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app: Flask) -> None:
    """Register application blueprints."""

    app.register_blueprint(health_blueprint)
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

