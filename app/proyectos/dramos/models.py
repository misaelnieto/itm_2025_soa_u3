"""Modelos de base de datos para productos."""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel  # type: ignore


def now_utc():
    """Obtiene la fecha y hora actual en UTC.

    Returns:
        datetime: La fecha y hora actual en UTC.

    """
    return datetime.now(UTC)


class Producto(SQLModel, table=True):
    """Modelo para registrar productos en la base de datos."""

    __tablename__ = "productos"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(title="Nombre", nullable=False)
    tipo: str = Field(title="Tipo", nullable=False)
    precio: float = Field(title="Precio", nullable=False)
    created_at: datetime = Field(
        title="Creado en",
        default_factory=now_utc,
        nullable=False,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "nombre": "Laptop Gamer",
                    "tipo": "Electrónica",
                    "precio": 1200.99,
                    "created_at": "2025-01-01T00:00:00",
                },
                {
                    "id": 2,
                    "nombre": "Zapatillas Deportivas",
                    "tipo": "Calzado",
                    "precio": 89.99,
                    "created_at": "2025-01-02T00:00:00",
                },
            ],
        },
    }