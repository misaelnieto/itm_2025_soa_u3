"""Modelos Pydantic y SQLModel para la API de Registro de Ciudades."""

from typing import ClassVar

from sqlmodel import Field, SQLModel


class CityBase(SQLModel):
    """Modelo base para los datos de una ciudad, sin 'table=True'."""
    
    name: str = Field(
        min_length=1,
        nullable=False,
        description="Nombre de la ciudad. No puede ser nulo ni vacío.",
    )
    population: int = Field(
        ge=0,
        nullable=False,
        description="Población de la ciudad. No puede ser nulo ni negativo.",
    )
    country: str = Field(
        min_length=1,
        nullable=False,
        description="País al que pertenece la ciudad. No puede ser nulo ni vacío.",
    )
    region: str | None = Field(
        default=None,
        min_length=1,
        nullable=True,
        description="Región o estado. Puede ser nulo, pero no vacío si se proporciona.",
    )

class City(CityBase, table=True):
    """Modelo que representa la tabla 'registro_ciudad' en la base de datos."""

    __tablename__: ClassVar[str] = "registro_ciudad"

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Identificador único de la ciudad generado por la base de datos.",
    )