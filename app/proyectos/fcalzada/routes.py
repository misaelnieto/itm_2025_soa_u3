"""Documentacion."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy import func
from sqlmodel import select

from app.db import DbSession

from .models import Car
from .schemas import CarroResponse, CarroResult, CarroType


async def calcular_inventario(db: DbSession) -> int:
    """Calcula el inventario total sumando las cantidades de todos los registros de carros en la base de datos.

    Args:- db (Session): La sesión de la base de datos usada para ejecutar la consulta.

    Returns:- int: El inventario total calculado a partir de la suma de las cantidades de todos los registros de carros.
           Retorna 0 si no hay registros.
    """
    result = db.exec(select(func.coalesce(func.sum(Car.quantity), 0)))
    return result.one_or_none()


api_router = APIRouter(
    prefix="/registro_carro",
    tags=["Registro de Carros"],
    responses={404: {"description": "No encontrado"}},
)

@api_router.get("/carros", tags=["Registro de Carros"])
def listar_carros(db: DbSession) -> list[Car]:
    """Recupera la lista de todos los registros de carros en **Registro de Carros**.

    Este endpoint devuelve todos los registros de carros registrados en la aplicación.

    - **Retorna**: `list[Car]`: Una lista de todos los registros de carros en la base de datos.
    """
    return db.exec(select(Car)).all()


@api_router.put("/registro/{tipo}/{cantidad}", tags=["Registro de Carros"], status_code=status.HTTP_201_CREATED)
async def registrar_carro(
    tipo: CarroType,
    cantidad: PositiveInt,
    marca: str,
    modelo: str,
    año: int,
    color: str,  # Se añade el atributo color
    db: DbSession,
    inventario: Annotated[int, Depends(calcular_inventario)],
) -> CarroResponse:
    """Crea un nuevo registro de carro (`entrada` o `salida`) en **Registro de Carros**.

    Este endpoint crea un nuevo registro de carro en la aplicación. Puede manejar
    tanto registros de entrada como de salida. Si el tipo de registro es `salida` y la cantidad excede el inventario
    actual, el registro será rechazado.

    **Args:**
    - `tipo` (`CarroType`): El tipo de registro (`"entrada"` o `"salida"`).
    - `cantidad` (`PositiveInt`): La cantidad para el registro.
    - `marca` (`str`): La marca del carro.
    - `modelo` (`str`): El modelo del carro.
    - `año` (`int`): El año del carro.
    - `color` (`str`): El color del carro.

    **Retorna:**
    - `CarroResponse`: La respuesta que contiene el resultado del registro,
      el inventario anterior y el nuevo inventario.

    **Lanza:**
    - `HTTPException`: Si el registro es una salida y la cantidad excede el inventario
      actual, se lanza un error 403 Forbidden con una respuesta de rechazo.
    """
    if tipo == CarroType.salida and cantidad > inventario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=CarroResponse(
                result=CarroResult.rechazado,
                previous_inventory=inventario,
                inventory=inventario,
            ).model_dump(),
        )
    
    # Operación: +1 para entrada, -1 para salida
    op = 1 if tipo == CarroType.entrada else -1
    db.add(Car(quantity=cantidad * op, marca=marca, modelo=modelo, año=año, color=color))  # Se añade 'color' aquí
    db.commit()

    nuevo_inventario = await calcular_inventario(db)
    
    return CarroResponse(
        result=CarroResult.registrado,
        previous_inventory=inventario,
        inventory=nuevo_inventario,
    )
