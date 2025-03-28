"""Modelos de base de datos para la API de animales.

Este módulo contiene los modelos SQLModel utilizados para definir
la estructura de las tablas en la base de datos para el registro de animales.
"""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def now_utc():
    """Obtiene la fecha y hora actual en UTC.
    
    Esta función se utiliza como valor predeterminado para el campo
    created_at en los modelos de base de datos.
    
    Returns:
        datetime: La fecha y hora actual en formato UTC.
    
    """
    return datetime.now(UTC)


class Register(SQLModel, table=True):
    """Modelo para registrar los animales en la base de datos.
    
    Esta clase define la estructura de la tabla 'animales' en la base de datos,
    incluyendo todos los campos necesarios para almacenar la información de un animal.
    """

    __tablename__ = "animales"  # Nombre de la tabla en la base de datos
    id: int | None = Field(default=None, primary_key=True)  # Identificador único del animal
    nombre: str = Field(title="Nombre", nullable=False)  # Nombre del animal
    raza: str = Field(title="Raza", nullable=False)  # Raza del animal
    edad: int = Field(title="Edad", nullable=False)  # Edad del animal
    created_at: datetime = Field(
        title="Created At",
        default_factory=now_utc,
        nullable=False,
    )  # Fecha y hora de registro del animal

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
