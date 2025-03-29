"""Esquemas de validación de datos."""

from datetime import datetime

from pydantic import BaseModel


class TransactionBase(BaseModel):
    """Base schema for a transaction."""

    id: int
    """Id of the student."""
    nombre: str
    """Name of the student."""
    carrera: str
    """career of the student."""

class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""

    nombre: str
    """Name of the student."""
    carrera: str
    """Career of the student."""
    
class TransactionRead(TransactionBase):
    """Schema for reading a transaction."""
    
    id: int
    """ID of the transaction."""
    
    created_at: datetime
    """Timestamp when the transaction was created."""

    class Config:
        """Configuration for ORM mode."""

        orm_mode = True



class Eliminado(BaseModel):
    """Message when the student is deleted."""

    message :  str