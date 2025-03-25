"""Esquemas de validación de datos."""

from datetime import datetime

from pydantic import BaseModel


class TransactionBase(BaseModel):
    """Base schema for a transaction."""

    isbn: int
    """ISBN of the book."""
    titulo: str
    """Title of the book."""
    autor: str
    """Author of the book."""


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""

    pass


class TransactionRead(TransactionBase):
    """Schema for reading a transaction."""

    id: int
    """ID of the transaction."""
    created_at: datetime
    """Timestamp when the transaction was created."""

    class Config:
        orm_mode = True
