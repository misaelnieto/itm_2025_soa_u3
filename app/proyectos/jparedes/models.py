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

    __tablename__ = "libreria_transaction"
    id: int | None = Field(default=None, primary_key=True)
    isbn: int = Field(title="ISBN", nullable=False)
    titulo: str = Field(title="Titulo", nullable=False)
    autor: str = Field(title="Autor", nullable=False)
    created_at: datetime = Field(
        title="Created At",
        default_factory=now_utc,
        nullable=False,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "isbn": 9789876123456,
                    "titulo": "El Aleph",
                    "autor": "Jorge Luis Borges",
                    "created_at": "2022-01-01T00:00:00",
                },
                {
                    "id": 2,
                    "isbn": 9789876543210,
                    "titulo": "Cien años de soledad",
                    "autor": "Gabriel García Márquez",
                    "created_at": "2022-01-02T00:00:00",
                },
            ],
        },
    }
