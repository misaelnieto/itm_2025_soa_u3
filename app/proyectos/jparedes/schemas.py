"""Esquemas de validación de datos."""

from datetime import datetime

from pydantic import BaseModel


class BookBase(BaseModel):
    """Base schema for a transaction."""

    isbn: int
    """ISBN of the book."""
    titulo: str
    """Title of the book."""
    autor: str
    """Author of the book."""


class BookCreate(BookBase):
    """Schema for creating a transaction."""


class BookRead(BookBase):
    """Schema for reading a transaction."""

    id: int
    """ID of the transaction."""
    created_at: datetime
    """Timestamp when the transaction was created."""

    class Config:
        """Configuration for ORM mode."""

        orm_mode = True
