"""All the database models here."""
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def now_utc():
    """Get the current UTC datetime.

    Returns:
        datetime: The current datetime in UTC.

    """
    return datetime.now(UTC)


class Transaction(SQLModel, table=True):
    """Modelo para registrar movimientos en la base de datos."""

    __tablename__ = "alcancia_transaction"
    id: int | None = Field(default=None, primary_key=True)
    amount: int = Field(title="Cantidad", nullable=False)
    created_at: datetime = Field(
        title="Created At",
        default_factory=now_utc,
        nullable=False,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "amount": -1000,
                    "id": 4,
                    "created_at": "2025-03-13T07:48:04.965275",
                },
                {"amount": 2500, "id": 5, "created_at": "2025-03-14T07:05:07.841158"},
            ],
        },
    }
