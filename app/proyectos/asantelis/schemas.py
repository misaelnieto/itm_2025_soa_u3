"""Esquemas de Pydantic para validación de datos de la API de animales.

Este módulo contiene los modelos de Pydantic utilizados para validar los datos
de entrada y salida en las operaciones CRUD de la API de animales.

"""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class AnimalCreate(BaseModel):
    """Esquema para la creación de un nuevo registro de animal.

    Este modelo valida los datos necesarios para crear un nuevo animal
    en la base de datos, asegurando que todos los campos requeridos
    estén presentes y sean válidos.

    """

    nombre: str
    """Nombre del animal (campo obligatorio)"""
    raza: str
    """Raza o especie del animal (campo obligatorio)"""
    edad: int = Field(..., ge=0)
    """Edad del animal en años (debe ser mayor o igual a 0)"""

    @field_validator("nombre", "raza", mode="before")
    @classmethod
    def validate_not_empty(cls, v):
        """Valida que los campos de texto no estén vacíos.

        Args:
            v: Valor del campo a validar

        Returns:
            El valor validado si es válido

        Raises:
            ValueError: Si el campo está vacío o solo contiene espacios

        """
        if not v or v.strip() == "":
            raise ValueError("field required")
        return v

    class Config:
        """Configuración adicional para el modelo AnimalCreate."""

        json_schema_extra = {
            "examples": [
                {
                    "nombre": "Firulais",
                    "raza": "Pastor Alemán",
                    "edad": 5,
                },
                {
                    "nombre": "Rex",
                    "raza": "Bulldog",
                    "edad": 3,
                },
            ],
        }


class AnimalUpdate(BaseModel):
    """Esquema para actualizar un animal existente.

    Este modelo permite actualizar parcialmente los datos de un animal,
    haciendo que todos los campos sean opcionales pero validando que
    si se proporcionan, sean válidos.

    """

    nombre: str | None = None
    """Nombre del animal (campo opcional)"""
    raza: str | None = None
    """Raza o especie del animal (campo opcional)"""
    edad: int | None = Field(None, ge=0)
    """Edad del animal en años (opcional, debe ser mayor o igual a 0 si se proporciona)"""

    @field_validator("nombre", "raza")
    @classmethod
    def validate_not_empty(cls, v):
        """Valida que los campos de texto no estén vacíos si se proporcionan.

        Args:
            v: Valor del campo a validar

        Returns:
            El valor validado si es válido o None

        Raises:
            ValueError: Si el campo proporcionado está vacío o solo contiene espacios

        """
        if v is not None and (not v or v.strip() == ""):
            raise ValueError("field required")
        return v

    class Config:
        """Configuración adicional para el modelo AnimalUpdate."""

        json_schema_extra = {
            "examples": [
                {
                    "nombre": "Firulais",
                    "raza": "Pastor Alemán",
                },
                {
                    "raza": "Bulldog",
                    "edad": 3,
                },
            ],
        }


class AnimalResponse(BaseModel):
    """Esquema para la respuesta de operaciones con animales.

    Este modelo define la estructura de los datos que se devuelven
    al cliente cuando se consulta información de un animal.

    """

    id: int
    """Identificador único del animal en la base de datos"""
    nombre: str
    """Nombre del animal"""
    raza: str
    """Raza o especie del animal"""
    edad: int
    """Edad del animal en años"""
    created_at: datetime
    """Fecha y hora de registro del animal en formato ISO 8601"""

    class Config:
        """Configuración adicional para el modelo AnimalResponse."""

        orm_mode = True
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 4,
                    "nombre": "Firulais",
                    "raza": "Pastor Alemán",
                    "edad": 5,
                    "created_at": "2025-03-13T07:48:04.965275",
                },
                {
                    "id": 5,
                    "nombre": "Rex",
                    "raza": "Bulldog",
                    "edad": 3,
                    "created_at": "2025-03-14T07:05:07.841158",
                },
            ],
        }
