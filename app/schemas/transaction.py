"""Schemas for transaction payloads."""
from __future__ import annotations

from datetime import datetime

from marshmallow import Schema, ValidationError, fields, validates, validates_schema

from ..models.transaction import SUPPORTED_CURRENCIES, TRANSACTION_TYPES


class TransactionSchema(Schema):
    """Serialize transaction entities."""

    id = fields.Int(dump_only=True)
    client_id = fields.Int(required=True)
    amount = fields.Decimal(as_string=True, required=True, places=2)
    currency = fields.Str(required=True)
    type = fields.Str(required=True)
    description = fields.Str(load_default=None)
    created_at = fields.DateTime(dump_only=True)


class TransactionCreateSchema(TransactionSchema):
    """Schema for creating transactions."""

    @validates("currency")
    def validate_currency(self, value: str) -> None:
        if value not in SUPPORTED_CURRENCIES:
            raise ValidationError(f"Unsupported currency '{value}'.")

    @validates("type")
    def validate_type(self, value: str) -> None:
        if value not in TRANSACTION_TYPES:
            raise ValidationError(f"Unsupported transaction type '{value}'.")

    @validates("amount")
    def validate_amount(self, value: object) -> None:
        if value is None:
            raise ValidationError("Amount is required.")
        if float(value) <= 0:
            raise ValidationError("Amount must be greater than zero.")


class TransactionUpdateSchema(Schema):
    """Schema for updating transactions."""

    amount = fields.Decimal(as_string=True, required=False, places=2)
    currency = fields.Str(required=False)
    type = fields.Str(required=False)
    description = fields.Str(required=False, allow_none=True)

    @validates_schema
    def validate_any_field(self, data: dict[str, object], **_: object) -> None:
        if not data:
            raise ValidationError("At least one field must be provided for update.")

    @validates("currency")
    def validate_currency(self, value: str) -> None:
        if value not in SUPPORTED_CURRENCIES:
            raise ValidationError(f"Unsupported currency '{value}'.")

    @validates("type")
    def validate_type(self, value: str) -> None:
        if value not in TRANSACTION_TYPES:
            raise ValidationError(f"Unsupported transaction type '{value}'.")

    @validates("amount")
    def validate_amount(self, value: object) -> None:
        if value is not None and float(value) <= 0:
            raise ValidationError("Amount must be greater than zero.")


class TransactionQuerySchema(Schema):
    """Schema for validating transaction listing filters."""

    client_id = fields.Int(load_default=None)
    type = fields.Str(load_default=None)
    start_date = fields.DateTime(load_default=None)
    end_date = fields.DateTime(load_default=None)

    @validates("type")
    def validate_type(self, value: str) -> None:
        if value is not None and value not in TRANSACTION_TYPES:
            raise ValidationError(f"Unsupported transaction type '{value}'.")

    @validates_schema
    def validate_date_range(self, data: dict[str, datetime], **_: object) -> None:
        start = data.get("start_date")
        end = data.get("end_date")
        if start and end and start > end:
            raise ValidationError("start_date must be before end_date.")

