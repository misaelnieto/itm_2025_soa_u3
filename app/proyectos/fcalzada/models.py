"""Documentacion."""
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def now_utc():
    """Obtener la fecha y hora actual en UTC.

    Returns: datetime: La fecha y hora actual en UTC.
    """
    return datetime.now(UTC)


class Car(SQLModel, table=True):
    """Modelo para registrar carros en la base de datos."""

    __tablename__ = "registro_carro"
    id: int | None = Field(default=None, primary_key=True)
    quantity: int = Field(title="Cantidad", nullable=False)  # 'quantity' para representar carros
    marca: str = Field(title="Marca", nullable=False)  # Atributo de marca
    modelo: str = Field(title="Modelo", nullable=False)  # Atributo de modelo
    año: int = Field(title="Año", nullable=False)  # Atributo de año
    color: str = Field(title="Color", nullable=False)  # Atributo de color
    created_at: datetime = Field(
        title="Fecha de Registro",
        default_factory=now_utc,
        nullable=False,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "quantity": 1,  # Ejemplo de registro de un carro
                    "id": 4,
                    "marca": "Toyota",
                    "modelo": "Corolla",
                    "año": 2020,
                    "color": "Rojo",
                    "created_at": "2025-03-13T07:48:04.965275",
                },
                {
                    "quantity": 2,
                    "id": 5,
                    "marca": "Honda",
                    "modelo": "Civic",
                    "año": 2021,
                    "color": "Negro",
                    "created_at": "2025-03-14T07:05:07.841158",
                },
            ],
        },
    }
