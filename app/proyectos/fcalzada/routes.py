"""Modulo de registro de carros."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlmodel import select

from app.db import DbSession

from .models import Car
from .schemas import CarroCreate, CarroResponse, CarroResult


async def calcular_inventario(db: DbSession) -> int:
    """Calcula el inventario total sumando las cantidades de todos los registros de carros en la base de datos."""
    result = db.exec(select(func.coalesce(func.sum(Car.quantity), 0)))
    return result.one_or_none()
"""Esta función realiza una consulta a la base de datos utilizando SQLAlchemy para obtener la suma total de la 
    cantidad de carros en el inventario, devolviendo el valor como un entero.
    
    Args:
        db (DbSession): La sesión de base de datos para realizar la consulta.
    
    Returns:
        int: El total de carros en el inventario.
    """

api_router = APIRouter(
    prefix="/registro_carro",
    tags=["Registro de Carros"],
    responses={404: {"description": "No encontrado"}},
)

##########################################################
##########################################################
@api_router.get("/carros", tags=["Registro de Carros"])
def listar_carros(db: DbSession) -> list[Car]:
    """Recupera la lista de todos los registros de carros en **Registro de Carros**."""
    return db.exec(select(Car)).all()

"""Este endpoint obtiene todos los carros registrados en el sistema y los devuelve como una lista de objetos `Car`.

    Args:
        db (DbSession): La sesión de base de datos para realizar la consulta.
    
    Returns:
        list[Car]: Una lista con todos los carros registrados.
    """

###########################################################################
###########################################################################
@api_router.post(
    "/registro/{tipo}", tags=["Registro de Carros"], status_code=status.HTTP_201_CREATED)  # antes PUT ahora POST
async def registrar_carro(
    tipo:str,
    request:CarroCreate,
    db: DbSession,
    inventario: Annotated[int, Depends(calcular_inventario)],
) -> CarroResponse:
    """Crea un nuevo registro de carro (`entrada` o `salida`) en **Registro de Carros**.

    Este endpoint maneja la creación de un nuevo registro de carro, ya sea para una entrada o una salida de carro del inventario.
    Si el tipo de registro es "salida" y la cantidad de carros a eliminar excede el inventario disponible, se rechazará la operación.
    
    Args:
        tipo (str): El tipo de operación, "entrada" para agregar un carro o "salida" para eliminar uno.
        request (CarroCreate): Datos del carro a registrar, incluyendo marca, modelo, año, y color.
        db (DbSession): La sesión de base de datos para realizar la operación.
        inventario (int): El inventario actual, obtenido a través de la dependencia `calcular_inventario`.
    
    Returns:
        CarroResponse: Respuesta que incluye el estado de la operación y el inventario actualizado.
    
    Raises:
        HTTPException: Si se intenta realizar una salida de carros cuando no hay suficientes en inventario.
    
    """
    cantidad = 1  # Fijamos la cantidad a 1, ya que solo se registrará 1 carro siempre

    # Validación de salida (no permitir salida si la cantidad es mayor que el inventario disponible)
    if tipo == "salida" and cantidad > inventario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=CarroResponse(
                result=CarroResult.rechazado,
                previous_inventory=inventario,
                inventory=inventario,
            ).model_dump(),
        )

    # Operación: +1 para entrada, -1 para salida
    op = 1 if tipo == "entrada" else -1
    db.add(Car(quantity=cantidad * op, marca=request.marca, modelo=request.modelo, año=request.año, color=request.color))  # Se añade 'color' aquí
    db.commit()

    nuevo_inventario = await calcular_inventario(db)

    return CarroResponse(
        result=CarroResult.registrado,
        previous_inventory=inventario,
        inventory=nuevo_inventario,
    )


###################################################################################
###################################################################################
@api_router.put("/actualizar/{id}", tags=["Registro de Carros"], status_code=status.HTTP_200_OK)
async def actualizar_carro(id: int, marca: str, modelo: str, año: int, color: str, db: DbSession) -> CarroResponse:
    """Actualiza un carro existente por ID.

    Este endpoint permite actualizar un carro registrado en el sistema, cambiando sus atributos como marca, modelo, año y color.

    Args:
        id (int): El ID del carro que se desea actualizar.
        marca (str): La nueva marca del carro.
        modelo (str): El nuevo modelo del carro.
        año (int): El nuevo año del carro.
        color (str): El nuevo color del carro.
        db (DbSession): La sesión de base de datos para realizar la operación.

    Returns:
        CarroResponse: Respuesta con el estado de la operación y el inventario actualizado.
    
    Raises:
        HTTPException: Si no se encuentra el carro con el ID proporcionado.
    
    """
    carro = db.get(Car, id)

    if not carro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontró el carro con ID {id}")

    # Actualizar campos
    carro.marca = marca
    carro.modelo = modelo
    carro.año = año
    carro.color = color

    db.add(carro)
    db.commit()

    nuevo_inventario = await calcular_inventario(db)

    return CarroResponse(result=CarroResult.registrado, previous_inventory=nuevo_inventario, inventory=nuevo_inventario)


@api_router.delete("/eliminar/{id}", tags=["Registro de Carros"], status_code=status.HTTP_200_OK)
async def eliminar_carro(id: int, db: DbSession) -> dict:  # noqa: A002
    """Elimina un carro por ID.

    Este endpoint elimina un carro registrado en el sistema por su ID.

    Args: id (int): El ID del carro que se desea eliminar.
        db (DbSession): La sesión de base de datos para realizar la operación.

    Returns: dict: Un mensaje indicando que el carro fue eliminado exitosamente.
    
    Raises: HTTPException: Si no se encuentra el carro con el ID proporcionado.
    """
    carro = db.get(Car, id)

    if not carro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontró el carro con ID {id}")

    db.delete(carro)
    db.commit()

    return {"message": f"Carro con ID {id} eliminado exitosamente"}
