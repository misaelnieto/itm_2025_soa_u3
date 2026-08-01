"""Esquemas y enumeraciones para el registro de carros."""
from enum import StrEnum

from pydantic import BaseModel


class CarroType(StrEnum):
    """Define el tipo de registro de carro.

    Tipos disponibles:
        - `entrada`: Registro de entrada de un carro al inventario.
        - `salida`: Registro de salida de un carro del inventario.
    """

    entrada = "entrada"  # Cambié 'deposit' a 'entrada'
    salida = "salida"    # Cambié 'withdraw' a 'salida'


class CarroResult(StrEnum):
    """Define los posibles resultados de un registro de carro.

    Resultados:
        - `registrado`: El registro fue exitoso.
        - `fallido`: El registro no pudo completarse.
        - `rechazado`: El registro fue rechazado (por ejemplo, falta de inventario).
    """

    registrado = "registrado"  # Cambié 'settled' a 'registrado'
    fallido = "fallido"        # Cambié 'failed' a 'fallido'
    rechazado = "rechazado"    # Cambié 'rejected' a 'rechazado'


class CarroResponse(BaseModel):
    """Representa la respuesta después de realizar un registro de carro.

    Atributos:
        result (CarroResult): Resultado del registro (`registrado`, `fallido` o `rechazado`).
        previous_inventory (int | None): Inventario antes del registro (opcional).
        inventory (int | None): Inventario después del registro (opcional).

    Ejemplos JSON:
        - Entrada exitosa:
        ```json
        {
            "result": "registrado",
            "previous_inventory": 5,
            "inventory": 6
        }
        ```

        - Salida exitosa:
        ```json
        {
            "result": "registrado",
            "previous_inventory": 5,
            "inventory": 4
        }
        ```

        - Registro rechazado por falta de inventario:
        ```json
        {
            "result": "rechazado",
            "previous_inventory": 5,
            "inventory": 5
        }
        ```
    """

    result: CarroResult
    """El resultado del registro de carro (`registrado`, `fallido` o `rechazado`)."""
    previous_inventory: int | None
    """Inventario antes del registro (opcional)."""
    inventory: int | None
    """Inventario después del registro (opcional)."""

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
    """Configuración adicional para mostrar ejemplos JSON en la documentación de la API."""

class CarroCreate(BaseModel):
    """Esquema para crear un nuevo registro de carro."""

    marca: str
    """Marca del carro."""
    modelo: str
    """Modelo del carro."""
    año: int
    """Año del carro."""
    color: str
    """Color del carro."""

   


class Carro(CarroCreate):
    """Esquema que representa un carro registrado en la base de datos."""

    id: int
    """ID del carro registrado."""

    class Config:  # noqa: D106
        orm_mode = True
        """Configuración para habilitar la compatibilidad con ORMs."""