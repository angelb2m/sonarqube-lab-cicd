"""Transaction database model."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db

TRANSACTION_TYPES = ("DEBIT", "CREDIT")
SUPPORTED_CURRENCIES = ("MXN", "USD", "EUR")


class Transaction(db.Model):
    """Represents a financial transaction."""

    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_transactions_amount_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"), index=True, nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    type: Mapped[str] = mapped_column(Enum(*TRANSACTION_TYPES, name="transaction_types"), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    client = relationship("Client", back_populates="transactions")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Transaction id={self.id} client_id={self.client_id} amount={self.amount}>"

