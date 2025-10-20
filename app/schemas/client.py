"""Schemas for client payloads."""
from __future__ import annotations

from marshmallow import Schema, ValidationError, fields, validates, validates_schema


class ClientSchema(Schema):
    """Serialize client entities."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)


class ClientCreateSchema(ClientSchema):
    """Schema for creating clients."""

    pass


class ClientUpdateSchema(Schema):
    """Schema for updating clients."""

    name = fields.Str(required=False)
    email = fields.Email(required=False)

    @validates_schema
    def validate_any_field(self, data: dict[str, object], **_: object) -> None:
        if not data:
            raise ValidationError("At least one field must be provided for update.")

    @validates("name")
    def validate_name(self, value: str) -> None:
        if not value.strip():
            raise ValidationError("Name cannot be empty.")

    @validates("email")
    def validate_email(self, value: str) -> None:
        if not value.strip():
            raise ValidationError("Email cannot be empty.")
