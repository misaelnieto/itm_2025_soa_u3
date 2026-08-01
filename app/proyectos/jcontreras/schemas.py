"""Esquemas de validación de datos para ventas."""



from pydantic import BaseModel


class SaleCreate(BaseModel):
    """Schema for creating a sale."""

    cliente: str 
    producto: str
    cantidad: int 
    precio: float
  

