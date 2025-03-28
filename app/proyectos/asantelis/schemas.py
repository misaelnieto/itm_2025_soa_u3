"""Esquemas de Pydantic para validación de datos de la API de animales."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class AnimalBase(BaseModel):
    """Esquema base para un animal."""

    nombre: str
    """Nombre del animal (campo obligatorio)"""
    raza: str
    """Raza o especie del animal (campo obligatorio)"""
    edad: int = Field(..., ge=0)
    """Edad del animal en años (debe ser mayor o igual a 0)"""

    @field_validator("nombre", "raza", mode="before")
    @classmethod
    def validate_not_empty(cls, v):
        """Valida que los campos de texto no estén vacíos."""
        if not v or v.strip() == "":
            raise ValueError("field required")
        return v


class AnimalCreate(AnimalBase):
    """Esquema para la creación de un nuevo registro de animal."""

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
    """Esquema para actualizar un animal existente."""

    nombre: str | None = None
    """Nombre del animal (campo opcional)"""
    raza: str | None = None
    """Raza o especie del animal (campo opcional)"""
    edad: int | None = Field(None, ge=0)
    """Edad del animal en años (opcional, debe ser mayor o igual a 0 si se proporciona)"""

    @field_validator("nombre", "raza")
    @classmethod
    def validate_not_empty(cls, v):
        """Valida que los campos de texto no estén vacíos si se proporcionan."""
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


class AnimalResponse(AnimalBase):
    """Esquema para la respuesta de operaciones con animales."""

    id: int
    """Identificador único del animal en la base de datos"""
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
