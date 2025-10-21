"""Pytest fixtures for application testing."""
from __future__ import annotations

from typing import Generator

import pytest
from flask import Flask

from app import create_app
from app.extensions import db


@pytest.fixture()
def app() -> Generator[Flask, None, None]:
    """Create and configure a test application."""

    application = create_app("testing")
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app: Flask):
    """Return a Flask test client for API requests."""

    return app.test_client()


@pytest.fixture()
def session(app: Flask):
    """Provide direct access to the database session."""

    return db.session

