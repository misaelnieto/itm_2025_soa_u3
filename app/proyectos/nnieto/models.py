from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def now():
    return datetime.now(timezone.utc)


class Alcancia(SQLModel, table=True):
    """Modelo para registrar diferentes alcancias"""

    __tablename__ = "alcancia_alcancias"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(
        title="El nombre de la alcancía",
        nullable=False,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 4,
                    "nombre": "Alcancia de Pedro"
                },
                {
                    "id": 7,
                    "nombre": "Alcancia de Janet"
                },
            ]
        }
    }


class Movimiento(SQLModel, table=True):
    """Modelo para registrar movimientos en la base de datos"""

    __tablename__ = "alcancia_movimientos"
    id: int | None = Field(default=None, primary_key=True)
    cantidad: int = Field(title="Cantidad", nullable=False)
    created_at: datetime = Field(
        title="Created At",
        default_factory=now,
        nullable=False,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cantidad": -1000,
                    "id": 4,
                    "created_at": "2025-03-13T07:48:04.965275",
                },
                {"cantidad": 2500, "id": 5, "created_at": "2025-03-14T07:05:07.841158"},
            ]
        }
    }
