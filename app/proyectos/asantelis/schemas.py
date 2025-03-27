"""Esquemas de validación de datos."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class AnimalCreate(BaseModel):
    """Schema for creating a new animal."""

    nombre: str
    """The name of the animal"""
    raza: str
    """The breed of the animal"""
    edad: int = Field(..., ge=0)
    """The age of the animal"""

    @field_validator("nombre", "raza", mode="before")
    @classmethod
    def validate_not_empty(cls, v):
        """Valida que los campos de texto no estén vacíos."""
        if not v or v.strip() == "":
            raise ValueError("field required")
        return v

    class Config:
        """Configuration for the AnimalCreate model."""

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
    """Schema for updating an existing animal."""

    nombre: str | None = None
    """The name of the animal"""
    raza: str | None = None
    """The breed of the animal"""
    edad: int | None = Field(None, ge=0)
    """The age of the animal"""

    @field_validator("nombre", "raza")
    @classmethod
    def validate_not_empty(cls, v):
        """Valida que los campos de texto no estén vacíos si se proporcionan."""
        if v is not None and (not v or v.strip() == ""):
            raise ValueError("field required")
        return v

    class Config:
        """Configuration for the AnimalUpdate model."""

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
    """Schema for the response of an animal registration."""

    id: int
    """The ID of the animal"""
    nombre: str
    """The name of the animal"""
    raza: str
    """The breed of the animal"""
    edad: int
    """The age of the animal"""
    created_at: datetime
    """The timestamp when the animal was registered"""

    class Config:
        """Configuration for the AnimalResponse model."""

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
