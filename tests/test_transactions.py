"""Tests for transaction endpoints."""
from __future__ import annotations

from flask.testing import FlaskClient


def create_client(client: FlaskClient, name: str, email: str) -> int:
    response = client.post("/api/v1/clients", json={"name": name, "email": email})
    return response.get_json()["id"]


def test_create_transaction_success(client: FlaskClient) -> None:
    client_id = create_client(client, "Dana", "dana@example.com")
    response = client.post(
        "/api/v1/transactions",
        json={
            "client_id": client_id,
            "amount": "50.00",
            "currency": "USD",
            "type": "DEBIT",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["client_id"] == client_id
    assert data["type"] == "DEBIT"


def test_create_transaction_missing_client(client: FlaskClient) -> None:
    response = client.post(
        "/api/v1/transactions",
        json={
            "client_id": 9999,
            "amount": "50.00",
            "currency": "USD",
            "type": "DEBIT",
        },
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["field"] == "client_id"


def test_update_transaction(client: FlaskClient) -> None:
    client_id = create_client(client, "Eve", "eve@example.com")
    create_resp = client.post(
        "/api/v1/transactions",
        json={
            "client_id": client_id,
            "amount": "25.00",
            "currency": "EUR",
            "type": "CREDIT",
        },
    )
    txn_id = create_resp.get_json()["id"]

    update_resp = client.put(
        f"/api/v1/transactions/{txn_id}",
        json={"amount": "30.00", "description": "Adjustment"},
    )
    assert update_resp.status_code == 200
    data = update_resp.get_json()
    assert data["amount"] == "30.00"
    assert data["description"] == "Adjustment"


def test_list_transactions_filters(client: FlaskClient) -> None:
    client_id = create_client(client, "Frank", "frank@example.com")
    for amount, txn_type in [("10.00", "DEBIT"), ("20.00", "CREDIT")]:
        client.post(
            "/api/v1/transactions",
            json={
                "client_id": client_id,
                "amount": amount,
                "currency": "MXN",
                "type": txn_type,
            },
        )

    response = client.get(
        "/api/v1/transactions",
        query_string={"client_id": client_id, "type": "DEBIT"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 1
    assert data["items"][0]["type"] == "DEBIT"

