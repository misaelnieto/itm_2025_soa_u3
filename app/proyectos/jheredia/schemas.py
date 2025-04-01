"""Esquemas y enumeraciones para el registro de ciudades."""

from enum import StrEnum

from pydantic import BaseModel, Field


class CityType(StrEnum):
    """Tipos de operaciones para el registro de ciudades."""

    entrada = "entrada"
    salida = "salida"

class CityResult(StrEnum):
    """Resultados de las operaciones en el registro de ciudades."""

    registrado = "registrado"
    fallido = "fallido"
    rechazado = "rechazado"

class CityCreate(BaseModel):
    """Esquema Pydantic para la creación de una nueva ciudad."""

    name: str = Field(..., min_length=1, description="El nombre de la ciudad no puede estar vacío.")
    population: int = Field(..., ge=0, description="La población debe ser un número positivo.")
    country: str = Field(..., description="El campo 'country' no puede estar vacío.")
    region: str | None = Field(None, description="Región opcional de la ciudad.")

class CityUpdate(BaseModel):
    """Esquema para actualizar una ciudad existente."""

    name: str = Field(..., min_length=1)
    population: int = Field(..., ge=0)
    country: str = Field(..., min_length=1)
    region: str | None = Field(None, min_length=1)

class CityRead(BaseModel):
    """Esquema para leer/devolver datos de una ciudad."""

    id: int
    name: str
    population: int
    country: str
    region: str | None

    class Config:
        """orm_mode = True  # Permite que el modelo funcione con SQLModel y SQLAlchemy."""

        from_attributes = True

class CityResponse(BaseModel):
    """Respuesta para las operaciones en el registro de ciudades (entrada o salida)."""

    result: CityResult
    previous_population: int | None
    population: int | None

class DeleteResponse(BaseModel):
    """Esquema para la respuesta de eliminación de una ciudad."""

    message: str
    