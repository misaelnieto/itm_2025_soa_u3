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

    __tablename__ = "estudiantes_transaction"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(title="Nombre", nullable=False)
    carrera: str = Field(title="Carrera", nullable=False)
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
                    "titulo": "Juan Paredes",
                    "carrera": "Ingeniería en sistemas",
                    "created_at": "2022-01-01T00:00:00",
                },
                {
                    "id": 2,
                    "nombre": "Diego Dueñas",
                    "carrera": "Ingeniería en sistemas",
                    "created_at": "2022-01-02T00:00:00",
                },
            ],
        },
    }