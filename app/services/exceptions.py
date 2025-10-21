"""Custom exceptions for the service layer."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ServiceError(Exception):
    """Base class for domain level exceptions."""

    message: str

    def __str__(self) -> str:  # pragma: no cover - convenience
        return self.message


@dataclass(slots=True)
class EntityNotFoundError(ServiceError):
    """Raised when an entity cannot be located."""

    entity: str


@dataclass(slots=True)
class ValidationError(ServiceError):
    """Raised when a business rule validation fails."""

    field: str | None = None