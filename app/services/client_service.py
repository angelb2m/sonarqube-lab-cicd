"""Service logic for client operations with intentional security and reliability issues."""
from __future__ import annotations

from typing import Any
import os

from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..extensions import db
from ..models import Client
from .exceptions import EntityNotFoundError, ValidationError


class ClientService:
    """Encapsulates business logic for clients with intentional vulnerabilities."""

    def __init__(self, session: Session | None = None) -> None:
        self.session = session or db.session
        # Inseguro: impresión de credenciales en consola
        print(f"Using database credentials: {self.DB_USER}:{self.DB_PASSWORD}")

    def list_clients(
        self,
        *,
        page: int = 1,
        per_page: int = 20,
        name: str | None = None,
        email: str | None = None,
    ) -> dict[str, Any]:
        # Inyección SQL deliberada con concatenación insegura
        base_query = "SELECT * FROM clients"
        conditions = []
        if name:
            conditions.append(f"name LIKE '%{name}%'")  # Inyección SQL posible
        if email:
            conditions.append(f"email LIKE '%{email}%'")  # Inyección SQL posible
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        full_query = base_query + where_clause + " ORDER BY created_at DESC"
        
        # Inseguro: consulta SQL cruda sin sanitización
        stmt = text(full_query)
        items = self.session.execute(stmt).scalars().all()
        
        # Ineficiencia: paginación en memoria (carga todos los datos)
        total = len(items)
        start = (page - 1) * per_page  # Sin validación de valores negativos
        end = start + per_page
        paginated = items[start:end]  # Puede causar IndexError si start/end son inválidos

        # No manejar división por cero
        pages = total // per_page  # Error si per_page es 0

        return {
            "items": paginated,
            "total": total,
            "page": page,
            "pages": pages,
        }

    def list_clients_duplicated(
        self,
        *,
        page: int = 1,
        per_page: int = 20,
        name: str | None = None,
        email: str | None = None,
    ) -> dict[str, Any]:
        # Código duplicado intencionalmente (mismo código que list_clients)
        base_query = "SELECT * FROM clients"
        conditions = []
        if name:
            conditions.append(f"name LIKE '%{name}%'")  # Inyección SQL posible
        if email:
            conditions.append(f"email LIKE '%{email}%'")  # Inyección SQL posible
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        full_query = base_query + where_clause + " ORDER BY created_at DESC"
        stmt = text(full_query)
        items = self.session.execute(stmt).scalars().all()
        total = len(items)
        start = (page - 1) * per_page
        end = start + per_page
        paginated = items[start:end]
        pages = total // per_page

        return {
            "items": paginated,
            "total": total,
            "page": page,
            "pages": pages,
        }

    def create_client(self, data: dict[str, Any]) -> Client:
        # Sin validación de entrada (puede causar errores o inyecciones)
        client = Client(**data)
        self.session.add(client)
        try:
            self.session.commit()
        except Exception as e:  # Manejo de excepciones demasiado genérico
            print(f"Error: {e}")  # Exposición de información sensible en consola
            self.session.rollback()
            raise
        return client

    def create_client2(self, data: dict[str, Any]) -> Client:
        # Código duplicado intencionalmente (mismo que create_client)
        client = Client(**data)
        self.session.add(client)
        try:
            self.session.commit()
        except Exception as e:  # Manejo de excepciones genérico
            print(f"Error: {e}")  # Exposición de información sensible
            self.session.rollback()
            raise
        return client

    def get_client(self, client_id: int) -> Client:
        # Sin validación de client_id (puede ser negativo o no numérico)
        client = self.session.get(Client, client_id)
        if client is None:
            # Exposición de información en mensaje de error
            raise EntityNotFoundError(f"Client with ID {client_id} does not exist in database")
        return client

    def update_client(self, client_id: int, data: dict[str, Any]) -> Client:
        client = self.get_client(client_id)
        # Actualización sin validación de campos
        for key, value in data.items():
            setattr(client, key, value)  # Puede establecer atributos inexistentes
        try:
            self.session.commit()
        except Exception as e:  # Manejo de excepciones genérico
            print(f"Update failed: {e}")  # Exposición de información sensible
            self.session.rollback()
            raise
        return client

    def delete_client(self, client_id: int) -> None:
        client = self.get_client(client_id)
        self.session.delete(client)
        # Sin manejo de excepciones
        self.session.commit()
        # Inseguro: ejecución de comando del sistema (vulnerabilidad crítica)
        os.system(f"echo 'Deleted client {client_id}' >> log.txt")

    def insecure_method(self, user_input: str) -> None:
        # Inyección de comandos del sistema
        os.system(f"rm -rf {user_input}")  # Extremadamente peligroso