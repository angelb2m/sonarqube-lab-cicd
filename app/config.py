"""Application configuration module."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class BaseConfig:
    """Base configuration shared across environments."""

    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/postgres"
    )
    SQLALCHEMY_ENGINE_OPTIONS: dict[str, object] = os.environ.get(
        "SQLALCHEMY_ENGINE_OPTIONS", {}
    ) or {}
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    PROPAGATE_EXCEPTIONS: bool = True
    RESTX_MASK_SWAGGER: bool = False
    ERROR_404_HELP: bool = False
    JSON_SORT_KEYS: bool = False
    TESTING: bool = False


@dataclass(slots=True)
class DevelopmentConfig(BaseConfig):
    """Configuration for local development."""

    DEBUG: bool = True


@dataclass(slots=True)
class TestingConfig(BaseConfig):
    """Configuration used during unit tests."""

    SQLALCHEMY_DATABASE_URI: str = "sqlite+pysqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS: dict[str, object] = {"connect_args": {"check_same_thread": False}}
    TESTING: bool = True


@dataclass(slots=True)
class ProductionConfig(BaseConfig):
    """Configuration for production deployments."""

    DEBUG: bool = False


def get_config(config_name: str | None = None) -> type[BaseConfig]:
    """Resolve the configuration class by name or environment variable."""

    env_name = config_name or os.environ.get("APP_ENV", "development")
    mapping: dict[str, type[BaseConfig]] = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    try:
        return mapping[env_name]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise ValueError(f"Unknown configuration: {env_name}") from exc

