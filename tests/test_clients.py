"""Tests for client endpoints."""
from __future__ import annotations

from flask.testing import FlaskClient

from app.extensions import db
from app.models import Client


def test_create_client_success(client: FlaskClient) -> None:
    response = client.post(
        "/api/v1/clients",
        json={"name": "Alice", "email": "alice@example.com"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


def test_create_client_duplicate_email(client: FlaskClient) -> None:
    client.post(
        "/api/v1/clients",
        json={"name": "Alice", "email": "alice@example.com"},
    )
    response = client.post(
        "/api/v1/clients",
        json={"name": "Bob", "email": "alice@example.com"},
    )
    assert response.status_code == 409
    data = response.get_json()
    assert data["field"] == "email"


def test_list_clients_filters(client: FlaskClient, session) -> None:
    session.add_all(
        [
            Client(name="Alice", email="alice@example.com"),
            Client(name="Bob", email="bob@example.com"),
        ]
    )
    db.session.commit()
    response = client.get("/api/v1/clients", query_string={"name": "Ali"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Alice"


def test_delete_client_cascades_transactions(client: FlaskClient, session) -> None:
    client_response = client.post(
        "/api/v1/clients",
        json={"name": "Charlie", "email": "charlie@example.com"},
    )
    client_id = client_response.get_json()["id"]

    txn_response = client.post(
        "/api/v1/transactions",
        json={
            "client_id": client_id,
            "amount": "100.00",
            "currency": "USD",
            "type": "CREDIT",
            "description": "Initial credit",
        },
    )
    assert txn_response.status_code == 201

    delete_response = client.delete(f"/api/v1/clients/{client_id}")
    assert delete_response.status_code == 204

    txn_list = client.get(
        "/api/v1/transactions",
        query_string={"client_id": client_id},
    )
    assert txn_list.status_code == 200
    assert txn_list.get_json()["total"] == 0

