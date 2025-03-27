"""All the database models here."""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def now_utc():
    """Get the current UTC datetime.

    Returns:
        datetime: The current datetime in UTC.

    """
    return datetime.now(UTC)


class Register(SQLModel, table=True):
    """Modelo para registrar los animales en la base de datos."""

    __tablename__ = "animales"  # Nombre de la tabla en la base de datos
    id: int | None = Field(default=None, primary_key=True)  # Identificador único del animal
    nombre: str = Field(title="Nombre", nullable=False)  # Nombre del animal
    raza: str = Field(title="Raza", nullable=False)  # Raza del animal
    edad: int = Field(title="Edad", nullable=False)  # Edad del animal
    created_at: datetime = Field(
        title="Created At",
        default_factory=now_utc,
        nullable=False,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Firulais",
                    "raza": "Pastor Alemán",
                    "edad": 5,
                    "id": 4,
                    "created_at": "2025-03-13T07:48:04.965275",
                },
                {"nombre": "Rex", "raza": "Bulldog", "edad": 3, "id": 5, "created_at": "2025-03-14T07:05:07.841158"},
            ],
        },
    }
