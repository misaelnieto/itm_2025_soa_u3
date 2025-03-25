"""Documentacion."""
from enum import StrEnum

from pydantic import BaseModel


class CarroType(StrEnum):
    """Define el tipo de registro de carro. Solo dos tipos en este momento."""

    entrada = "entrada"  # Cambié 'deposit' a 'entrada'
    salida = "salida"    # Cambié 'withdraw' a 'salida'


class CarroResult(StrEnum):
    """El resultado del registro de carro."""

    registrado = "registrado"  # Cambié 'settled' a 'registrado'
    fallido = "fallido"        # Cambié 'failed' a 'fallido'
    rechazado = "rechazado"    # Cambié 'rejected' a 'rechazado'


class CarroResponse(BaseModel):
    """Representa el resultado del registro de carro."""

    result: CarroResult
    """El resultado de este registro de carro"""
    previous_inventory: int | None
    """El inventario antes de realizar el registro"""
    inventory: int | None
    """El inventario después de realizar el registro"""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "result": "registrado",
                    "previous_inventory": 5,
                    "inventory": 6,  # Ejemplo de entrada de un carro
                },
                {
                    "result": "registrado",
                    "previous_inventory": 5,
                    "inventory": 4,  # Ejemplo de salida de un carro
                },
                {
                    "result": "rechazado",
                    "previous_inventory": 5,
                    "inventory": 5,  # Ejemplo de rechazo por falta de inventario
                },
            ],
        },
    }


class CarroCreate(BaseModel):
    """Esquema para crear un nuevo registro de carro."""

    cantidad: int
    """Cantidad de carros para registrar."""
    marca: str
    """Marca del carro."""
    modelo: str
    """Modelo del carro."""
    año: int
    """Año del carro."""
    color: str
    """Color del carro."""

    class Config:  # noqa: D106
        orm_mode = True


class Carro(CarroCreate):
    """Esquema que representa un carro registrado en la base de datos."""

    id: int
    """ID del carro registrado."""
    created_at: str
    """Fecha de registro del carro."""

    class Config:  # noqa: D106
        orm_mode = True
