"""Client API resources."""
from __future__ import annotations

from flask import request
from flask_restx import Namespace, Resource, fields

from ..schemas import ClientCreateSchema, ClientSchema, ClientUpdateSchema
from ..services import ClientService

ns = Namespace("clients", description="Operations related to clients")

client_model = ns.model(
    "Client",
    {
        "id": fields.Integer(readOnly=True, description="Client identifier"),
        "name": fields.String(required=True, description="Client name"),
        "email": fields.String(required=True, description="Client email"),
        "created_at": fields.DateTime(readOnly=True),
    },
)

client_create_model = ns.model(
    "ClientCreate",
    {
        "name": fields.String(required=True, description="Client name"),
        "email": fields.String(required=True, description="Client email"),
    },
)

client_update_model = ns.model(
    "ClientUpdate",
    {
        "name": fields.String(required=False, description="Client name"),
        "email": fields.String(required=False, description="Client email"),
    },
)

pagination_model = ns.model(
    "ClientList",
    {
        "items": fields.List(fields.Nested(client_model)),
        "total": fields.Integer(),
        "page": fields.Integer(),
        "pages": fields.Integer(),
    },
)

client_schema = ClientSchema()
client_create_schema = ClientCreateSchema()
client_update_schema = ClientUpdateSchema()
service = ClientService()


@ns.route("")
class ClientCollection(Resource):
    """Collection resource for clients."""

    @ns.marshal_with(pagination_model)
    @ns.doc(
        params={
            "page": "Page number",
            "per_page": "Items per page",
            "name": "Filter by name",
            "email": "Filter by email",
        }
    )
    def get(self):  # type: ignore[override]
        """List clients with pagination and filters."""

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        name = request.args.get("name")
        email = request.args.get("email")
        result = service.list_clients(page=page, per_page=per_page, name=name, email=email)
        result["items"] = client_schema.dump(result["items"], many=True)
        return result

    @ns.expect(client_create_model, validate=True)
    @ns.marshal_with(client_model, code=201)
    def post(self):  # type: ignore[override]
        """Create a new client."""

        payload = client_create_schema.load(request.get_json())
        client = service.create_client(payload)
        return client_schema.dump(client), 201


@ns.route("/<int:client_id>")
@ns.param("client_id", "The client identifier")
class ClientItem(Resource):
    """Single client resource."""

    @ns.marshal_with(client_model)
    def get(self, client_id: int):  # type: ignore[override]
        """Retrieve a client."""

        client = service.get_client(client_id)
        return client_schema.dump(client)

    @ns.expect(client_update_model, validate=True)
    @ns.marshal_with(client_model)
    def put(self, client_id: int):  # type: ignore[override]
        """Update an existing client."""

        payload = client_update_schema.load(request.get_json())
        client = service.update_client(client_id, payload)
        return client_schema.dump(client)

    @ns.response(204, "Client deleted")
    def delete(self, client_id: int):  # type: ignore[override]
        """Delete a client."""

        service.delete_client(client_id)
        return "", 204


@ns.route("/<int:client_id>/transactions")
@ns.param("client_id", "The client identifier")
class ClientTransactions(Resource):
    """Transactions belonging to a client."""

    @ns.doc(params={"page": "Page number", "per_page": "Items per page"})
    def get(self, client_id: int):  # type: ignore[override]
        """List transactions for a client."""

        from ..schemas import TransactionSchema
        from ..services import TransactionService

        txn_service = TransactionService()
        txn_schema = TransactionSchema()

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        result = txn_service.list_client_transactions(
            client_id=client_id, page=page, per_page=per_page
        )
        result["items"] = txn_schema.dump(result["items"], many=True)
        return result

