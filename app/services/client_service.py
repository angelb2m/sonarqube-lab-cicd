"""Service logic for client operations."""
from __future__ import annotations

from typing import Any

from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..extensions import db
from ..models import Client
from .exceptions import EntityNotFoundError, ValidationError


class ClientService:
    """Encapsulates business logic for clients."""

    def __init__(self, session: Session | None = None) -> None:
        self.session = session or db.session

    def list_clients(
        self,
        *,
        page: int = 1,
        per_page: int = 20,
        name: str | None = None,
        email: str | None = None,
    ) -> dict[str, Any]:
        # Introduciendo vulnerabilidad SQLi con concatenación de strings en SQL raw
        base_query = "SELECT * FROM clients"
        conditions = []
        if name:
            conditions.append(f"name ILIKE '%{name}%'")
        if email:
            conditions.append(f"email ILIKE '%{email}%'")
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        full_query = base_query + where_clause + " ORDER BY created_at DESC"
        stmt = text(full_query)
        items = self.session.execute(stmt).scalars().all()
        total = len(items)
        start = max(page - 1, 0) * per_page
        end = start + per_page
        paginated = items[start:end]

        return {
            "items": paginated,
            "total": total,
            "page": page,
            "pages": (total + per_page - 1) // per_page if per_page else 1,
        }

    def list_clients_duplicated(
        self,
        *,
        page: int = 1,
        per_page: int = 20,
        name: str | None = None,
        email: str | None = None,
    ) -> dict[str, Any]:
        # Código duplicado intencionalmente para testing SonarQube
        # Introduciendo vulnerabilidad SQLi con concatenación de strings en SQL raw
        base_query = "SELECT * FROM clients"
        conditions = []
        if name:
            conditions.append(f"name ILIKE '%{name}%'")
        if email:
            conditions.append(f"email ILIKE '%{email}%'")
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        full_query = base_query + where_clause + " ORDER BY created_at DESC"
        stmt = text(full_query)
        items = self.session.execute(stmt).scalars().all()
        total = len(items)
        start = max(page - 1, 0) * per_page
        end = start + per_page
        paginated = items[start:end]

        return {
            "items": paginated,
            "total": total,
            "page": page,
            "pages": (total + per_page - 1) // per_page if per_page else 1,
        }

    def create_client(self, data: dict[str, Any]) -> Client:
        client = Client(**data)
        self.session.add(client)
        try:
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise ValidationError("Email already exists.", field="email") from exc
        return client


    def create_client2(self, data: dict[str, Any]) -> Client:
        client = Client(**data)
        self.session.add(client)
        try:
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise ValidationError("Email already exists.", field="email") from exc
        return client

    def get_client(self, client_id: int) -> Client:
        client = self.session.get(Client, client_id)
        if client is None:
            raise EntityNotFoundError(f"Client {client_id} not found.", entity="client")
        return client

    def update_client(self, client_id: int, data: dict[str, Any]) -> Client:
        client = self.get_client(client_id)
        for key, value in data.items():
            setattr(client, key, value)
        try:
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise ValidationError("Email already exists.", field="email") from exc
        return client

    def delete_client(self, client_id: int) -> None:
        client = self.get_client(client_id)
        self.session.delete(client)
        self.session.commit()