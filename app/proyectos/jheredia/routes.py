"""Rutas de FastAPI para el Registro de Ciudades."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlmodel import select

# Assuming DbSession is correctly typed Session from app.db
from app.db import DbSession

from .models import City
from .schemas import (
    CityCreate,
    CityResponse,
    CityResult,
    CityType,
    CityUpdate,
    DeleteResponse,
)


async def calcular_poblacion_total(db: DbSession) -> int:
    """Calcula la población total sumando las poblaciones de todas las ciudades registradas.

    Args:
        db (DbSession): Sesión de la base de datos.

    Returns:
        int: La población total calculada.

    """
    population_sum = db.query(func.sum(City.population)).scalar()  # Obtener directamente el valor entero
    return population_sum if population_sum is not None else 0  # Retornar 0 si es None


api_router = APIRouter(
    prefix="/registro_ciudades",
    tags=["Registro de Ciudades"],
    responses={404: {"description": "No encontrado"}},
)


@api_router.get("/ciudades", tags=["Registro de Ciudades"])
def listar_ciudades(db: DbSession) -> list[City]:
    """Retorna una lista de todas las ciudades registradas en el sistema.

    Args:
        db (DbSession): Sesión de la base de datos.

    Returns:
        list[City]: Lista de objetos City registrados.

    """
    return db.exec(select(City)).all()


@api_router.post(
    "/registro/{tipo}",
    tags=["Registro de Ciudades"],
    status_code=status.HTTP_201_CREATED,
)
async def registrar_ciudad(
    tipo: CityType,
    request: CityCreate,
    db: DbSession,
    poblacion_total: Annotated[int, Depends(calcular_poblacion_total)],
) -> CityResponse:
    """Crea un nuevo registro de ciudad, ya sea de 'entrada' o 'salida'.

    Args:
        tipo (CityType): Tipo de registro ('entrada' o 'salida').
        request (CityCreate): Datos de la ciudad a registrar.
        db (DbSession): Sesión de la base de datos.
        poblacion_total (int): Población total calculada.

    Returns:
        CityResponse: Respuesta con el resultado del registro.

    """
    if tipo == CityType.salida and request.population > poblacion_total:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Población a eliminar supera la población total disponible.",
        )

    op = 1 if tipo == CityType.entrada else -1

    if request.population < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Population in request cannot be negative.",
        )

    nueva_ciudad = City(
        name=request.name,
        population=request.population * op,
        country=request.country,
        region=request.region,
    )
    db.add(nueva_ciudad)
    db.commit()
    db.refresh(nueva_ciudad)

    nueva_poblacion_total = await calcular_poblacion_total(db)

    return CityResponse(
        result=CityResult.registrado,
        previous_population=poblacion_total,
        population=nueva_poblacion_total,
    )


@api_router.post(
    "/ciudades",
    tags=["Registro de Ciudades"],
    status_code=status.HTTP_201_CREATED,
)
async def crear_ciudad(
    request: CityCreate,
    db: DbSession,
) -> dict:
    """Crea una nueva ciudad en la base de datos.

    Args:
        request (CityCreate): Datos de la ciudad a crear.
        db (DbSession): Sesión de la base de datos.

    Returns:
        dict: Datos de la ciudad creada.

    """
    if not request.country or not request.country.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Country field cannot be empty or contain only spaces.",
        )

    if request.population < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Population cannot be negative for direct creation.",
        )

    nueva_ciudad = City(
        name=request.name,
        population=request.population,
        country=request.country,
        region=request.region,
    )
    db.add(nueva_ciudad)
    db.commit()
    db.refresh(nueva_ciudad)

    return {
        "id": nueva_ciudad.id,
        "name": nueva_ciudad.name,
        "population": nueva_ciudad.population,
        "country": nueva_ciudad.country,
        "region": nueva_ciudad.region,
    }


@api_router.put(
    "/actualizar/{city_id}",
    tags=["Registro de Ciudades"],
    status_code=status.HTTP_200_OK,
)
async def actualizar_ciudad(
    city_id: int,
    request: CityUpdate,
    db: DbSession,
) -> dict:
    """Actualiza los datos de una ciudad existente por su ID.

    Args:
        city_id (int): Identificador de la ciudad a actualizar.
        request (CityUpdate): Datos actualizados de la ciudad.
        db (DbSession): Sesión de la base de datos.

    Returns:
        dict: Datos de la ciudad actualizada.

    """
    ciudad = db.get(City, city_id)
    if not ciudad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró la ciudad con identificador {city_id}",
        )

    update_data = request.model_dump(exclude_unset=False)
    for key, value in update_data.items():
        setattr(ciudad, key, value)

    db.add(ciudad)
    db.commit()
    db.refresh(ciudad)

    return {
        "id": ciudad.id,
        "name": ciudad.name,
        "population": ciudad.population,
        "country": ciudad.country,
        "region": ciudad.region,
        "result": "registrado",
    }


@api_router.get(
    "/ciudades/{city_id}",
    tags=["Registro de Ciudades"],
    status_code=status.HTTP_200_OK,
)
async def obtener_ciudad(
    city_id: int,
    db: DbSession,
) -> dict:
    """Obtiene los datos de una ciudad específica por su identificador.

    Args:
        city_id (int): Identificador de la ciudad.
        db (DbSession): Sesión de la base de datos.

    Returns:
        dict: Datos de la ciudad encontrada.

    """
    ciudad = db.get(City, city_id)
    if not ciudad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró la ciudad con identificador {city_id}",
        )

    return {
        "id": ciudad.id,
        "name": ciudad.name,
        "population": ciudad.population,
        "country": ciudad.country,
        "region": ciudad.region,
    }


@api_router.delete(
    "/eliminar/{city_id}",
    tags=["Registro de Ciudades"],
    status_code=status.HTTP_200_OK,
)
async def eliminar_ciudad(
    city_id: int,
    db: DbSession,
) -> DeleteResponse:
    """Elimina una ciudad de la base de datos a partir de su identificador.

    Args:
        city_id (int): Identificador de la ciudad a eliminar.
        db (DbSession): Sesión de la base de datos.

    Returns:
        DeleteResponse: Mensaje de confirmación de eliminación.

    """
    ciudad = db.get(City, city_id)
    if not ciudad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró la ciudad con identificador {city_id}",
        )

    db.delete(ciudad)
    db.commit()

    return DeleteResponse(
        message=f"La ciudad con ID {city_id} ha sido eliminada exitosamente.",
    )
