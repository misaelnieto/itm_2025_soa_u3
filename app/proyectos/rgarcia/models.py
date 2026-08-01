"""All the database models here."""
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def now_utc():
    """Get the current UTC datetime.

    Returns:
        datetime: The current datetime in UTC.

    """
    return datetime.now(UTC)

class Receta(SQLModel, table=True):
    """Modelo para registrar movimientos en la base de datos."""

    __tablename__ = "receta"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(title="Nombre", nullable=False)
    descripcion: str = Field(title="Descripción", nullable=False)
    min_preparacion: int = Field(title="Minutos de Preparación", nullable=False)
    created_at: datetime = Field(
        title="Created At",
        default_factory=datetime.utcnow,
        nullable=False,
    )
    ingredientes: str = Field(title="Ingredientes", nullable=True)  
    metodo_preparacion: str = Field(title="Método de Preparación", nullable=True)  
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Tacos al Pastor",
                    "id": 1,
                    "descripcion": "Tacos de carne de cerdo adobada con piña",
                    "min_preparacion": 90,
                    "ingredientes": "500 gr de Carne de Cerdo, Piña",  
                    "metodo_preparacion": "Cocinar la carne, agregar la piña, servir en tortillas",  
                },
                {
                    "nombre": "Pizza",
                    "id": 2,
                    "descripcion": "Pizza de peperoni",
                    "min_preparacion": 120,
                    "ingredientes": "Masa para pizza, Queso mozzarella, Pepperoni",
                    "metodo_preparacion": "Preparar la masa, agregar queso y pepperoni, hornear",
                },
            ],
        },
    }
