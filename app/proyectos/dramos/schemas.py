"""Esquemas de validación de datos."""

from datetime import datetime

from pydantic import BaseModel


class ProductoBase(BaseModel):
    """Base schema for a product."""

    nombre: str
    """Name of the product."""
    tipo: str
    """Type of the product."""
    precio: float
    """Price of the product."""


class ProductoCreate(ProductoBase):
    """Schema for creating a product."""

    pass  # noqa: PIE790

class ProductoRead(ProductoBase):
    """Schema for reading a product."""

    id: int
    """ID of the product."""
    created_at: datetime
    """Timestamp when the product was created."""

    class Config:  # noqa: D106
        orm_mode = True