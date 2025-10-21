"""Health check endpoint."""
from __future__ import annotations

from flask import Blueprint, jsonify

health_blueprint = Blueprint("health", __name__)


@health_blueprint.get("/health")
def health() -> tuple[dict[str, str], int]:
    """Return application health information."""

    return jsonify({"status": "ok"}), 200

