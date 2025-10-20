"""Centralized instances of Flask extensions."""
from __future__ import annotations

from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title="Flask CRUD Demo API",
    version="1.0.0",
    description="REST API for managing clients and their transactions.",
    doc="/docs",
)

