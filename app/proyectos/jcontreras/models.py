"""Modelo de la base de datos para ventas."""


from sqlmodel import Field, SQLModel


class Sale(SQLModel, table=True):
    """Modelo para registrar ventas en la base de datos."""

    __tablename__ = "ventas"

    id: int | None = Field(default=None, primary_key=True)
    cliente: str = Field(title="Cliente", nullable=False)
    producto: str = Field(title="Producto", nullable=False)
    cantidad: int = Field(title="Cantidad", nullable=False)
    precio: float = Field(title="Precio", nullable=False)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "cliente": "Juan Pérez",
                    "producto": "Laptop Dell",
                    "cantidad": 2,
                    "precio": 15000.00,
                },
                {
                    "id": 2,
                    "cliente": "Ana González",
                    "producto": "Monitor LG",
                    "cantidad": 1,
                    "precio": 5000.00,
                    "created_at": "2025-03-26T00:00:00",
                },
            ],
        },
    }
