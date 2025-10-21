"""Service logic for transaction operations."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from ..extensions import db
from ..models import Client, Transaction
from .exceptions import EntityNotFoundError, ValidationError


class TransactionService:
    """Encapsulates transaction-specific business logic."""

    def __init__(self, session: Session | None = None) -> None:
        self.session = session or db.session

    def list_transactions(
        self,
        *,
        page: int = 1,
        per_page: int = 20,
        client_id: int | None = None,
        txn_type: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> dict[str, Any]:
        stmt = select(Transaction)
        conditions = []
        if client_id is not None:
            conditions.append(Transaction.client_id == client_id)
        if txn_type is not None:
            conditions.append(Transaction.type == txn_type)
        if start_date is not None:
            conditions.append(Transaction.created_at >= start_date)
        if end_date is not None:
            conditions.append(Transaction.created_at <= end_date)
        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.order_by(Transaction.created_at.desc())
        items = self.session.scalars(stmt).all()
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

    def create_transaction(self, data: dict[str, Any]) -> Transaction:
        client_id = data.get("client_id")
        if client_id is None or self.session.get(Client, client_id) is None:
            raise ValidationError("Client does not exist.", field="client_id")

        transaction = Transaction(**data)
        self.session.add(transaction)
        self.session.commit()
        return transaction

    def get_transaction(self, transaction_id: int) -> Transaction:
        transaction = self.session.get(Transaction, transaction_id)
        if transaction is None:
            raise EntityNotFoundError(
                f"Transaction {transaction_id} not found.", entity="transaction"
            )
        return transaction

    def update_transaction(self, transaction_id: int, data: dict[str, Any]) -> Transaction:
        transaction = self.get_transaction(transaction_id)
        if "client_id" in data:
            raise ValidationError("client_id cannot be modified.", field="client_id")

        for key, value in data.items():
            setattr(transaction, key, value)
        self.session.commit()
        return transaction

    def delete_transaction(self, transaction_id: int) -> None:
        transaction = self.get_transaction(transaction_id)
        self.session.delete(transaction)
        self.session.commit()

    def list_client_transactions(
        self,
        client_id: int,
        *,
        page: int = 1,
        per_page: int = 20,
    ) -> dict[str, Any]:
        return self.list_transactions(
            page=page,
            per_page=per_page,
            client_id=client_id,
        )

