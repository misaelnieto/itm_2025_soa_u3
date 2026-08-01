"""Esquemas de validación de datos."""
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, EmailStr


class ClientUpdate(BaseModel):
    """Schema for updating client information."""

    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    room: int | None = None
    check_in: datetime | None = None
    
class OperationType(StrEnum):
    """Defines the operation type."""

    add = 'add'
    delete = 'delete'
    update = 'update'
    search = 'search'
    list = 'list'
    
class OperationResult(StrEnum):
	"""The operation result."""
	
	success = 'success'
	failed = 'failed'
	rejected = 'rejected'

class OperationResponse(BaseModel):
	"""Represents the result of an operation."""
	
	result: OperationResult
	"""The result of this operation"""
	previous_data: dict|None
	"""The data before the operation takes place"""
	data: dict|None
	"""The data after the operation takes place"""