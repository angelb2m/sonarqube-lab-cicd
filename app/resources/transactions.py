"""Transaction API resources."""
from __future__ import annotations

from flask import request
from flask_restx import Namespace, Resource, fields

from ..schemas import (
    TransactionCreateSchema,
    TransactionQuerySchema,
    TransactionSchema,
    TransactionUpdateSchema,
)
from ..services import TransactionService

ns = Namespace("transactions", description="Operations related to transactions")

transaction_model = ns.model(
    "Transaction",
    {
        "id": fields.Integer(readOnly=True),
        "client_id": fields.Integer(required=True),
        "amount": fields.String(required=True, description="Decimal amount"),
        "currency": fields.String(required=True),
        "type": fields.String(required=True, enum=["DEBIT", "CREDIT"]),
        "description": fields.String(required=False),
        "created_at": fields.DateTime(readOnly=True),
    },
)

transaction_create_model = ns.model(
    "TransactionCreate",
    {
        "client_id": fields.Integer(required=True),
        "amount": fields.String(required=True, description="Decimal amount"),
        "currency": fields.String(required=True, enum=["MXN", "USD", "EUR"]),
        "type": fields.String(required=True, enum=["DEBIT", "CREDIT"]),
        "description": fields.String(required=False),
    },
)

transaction_update_model = ns.model(
    "TransactionUpdate",
    {
        "amount": fields.String(required=False, description="Decimal amount"),
        "currency": fields.String(required=False, enum=["MXN", "USD", "EUR"]),
        "type": fields.String(required=False, enum=["DEBIT", "CREDIT"]),
        "description": fields.String(required=False),
    },
)

transaction_list_model = ns.model(
    "TransactionList",
    {
        "items": fields.List(fields.Nested(transaction_model)),
        "total": fields.Integer(),
        "page": fields.Integer(),
        "pages": fields.Integer(),
    },
)

transaction_schema = TransactionSchema()
transaction_create_schema = TransactionCreateSchema()
transaction_update_schema = TransactionUpdateSchema()
transaction_query_schema = TransactionQuerySchema()
service = TransactionService()


@ns.route("")
class TransactionCollection(Resource):
    """Collection resource for transactions."""

    @ns.marshal_with(transaction_list_model)
    @ns.doc(
        params={
            "page": "Page number",
            "per_page": "Items per page",
            "client_id": "Filter by client id",
            "type": "Filter by transaction type",
            "start_date": "Filter by start datetime",
            "end_date": "Filter by end datetime",
        }
    )
    def get(self):  # type: ignore[override]
        """List transactions with filters."""

        args = transaction_query_schema.load(request.args.to_dict())
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        result = service.list_transactions(
            page=page,
            per_page=per_page,
            client_id=args.get("client_id"),
            txn_type=args.get("type"),
            start_date=args.get("start_date"),
            end_date=args.get("end_date"),
        )
        result["items"] = transaction_schema.dump(result["items"], many=True)
        return result

    @ns.expect(transaction_create_model, validate=True)
    @ns.marshal_with(transaction_model, code=201)
    def post(self):  # type: ignore[override]
        """Create a new transaction."""

        payload = transaction_create_schema.load(request.get_json())
        transaction = service.create_transaction(payload)
        return transaction_schema.dump(transaction), 201


@ns.route("/<int:transaction_id>")
@ns.param("transaction_id", "The transaction identifier")
class TransactionItem(Resource):
    """Single transaction resource."""

    @ns.marshal_with(transaction_model)
    def get(self, transaction_id: int):  # type: ignore[override]
        """Retrieve a transaction by id."""

        transaction = service.get_transaction(transaction_id)
        return transaction_schema.dump(transaction)

    @ns.expect(transaction_update_model, validate=True)
    @ns.marshal_with(transaction_model)
    def put(self, transaction_id: int):  # type: ignore[override]
        """Update a transaction."""

        payload = transaction_update_schema.load(request.get_json())
        transaction = service.update_transaction(transaction_id, payload)
        return transaction_schema.dump(transaction)

    @ns.response(204, "Transaction deleted")
    def delete(self, transaction_id: int):  # type: ignore[override]
        """Delete a transaction."""

        service.delete_transaction(transaction_id)
        return "", 204

