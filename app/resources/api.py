"""REST API blueprint and namespace registration."""
from __future__ import annotations

from flask import Blueprint
from marshmallow import ValidationError as MarshmallowValidationError

from ..extensions import api
from ..services import EntityNotFoundError, ValidationError
from .clients import ns as clients_namespace
from .transactions import ns as transactions_namespace

api_blueprint = Blueprint("api", __name__)
api.init_app(api_blueprint)
api.add_namespace(clients_namespace)
api.add_namespace(transactions_namespace)


@api.errorhandler(EntityNotFoundError)
def handle_not_found(error: EntityNotFoundError):
    """Convert domain not found errors into HTTP 404 responses."""

    return {"message": error.message, "entity": error.entity}, 404


@api.errorhandler(ValidationError)
def handle_validation(error: ValidationError):
    """Convert service validation errors into HTTP 400/409 responses."""

    status = 409 if error.field == "email" else 400
    payload = {"message": error.message}
    if error.field:
        payload["field"] = error.field
    return payload, status


@api.errorhandler(MarshmallowValidationError)
def handle_marshmallow(error: MarshmallowValidationError):
    """Transform marshmallow validation errors into HTTP 400 responses."""

    return {"message": "Validation error", "errors": error.messages}, 400

