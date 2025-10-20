"""WSGI entry point for running the application with gunicorn."""
from __future__ import annotations

from app import create_app

app = create_app()
