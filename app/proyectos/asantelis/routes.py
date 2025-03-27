"""API routes for managing animal registrations.

Routes:
    - `GET /animales`: Retrieve the list of all registered animals.
    - `POST /animales`: Register a new animal.
    - `GET /animales/{animal_id}`: Retrieve details of a specific animal.
    - `PUT /animales/{animal_id}`: Update details of a specific animal.
    - `DELETE /animales/{animal_id}`: Delete a specific animal registration.

Functions:
    - `animals_list`: Retrieve the list of all registered animals.
    - `create_animal`: Register a new animal.
    - `get_animal`: Retrieve details of a specific animal.
    - `update_animal`: Update details of a specific animal.
    - `delete_animal`: Delete a specific animal registration.

Dependencies:
    - [fastapi](https://fastapi.tiangolo.com/): FastAPI framework for building APIs.
    - [pydantic](https://docs.pydantic.dev/): Data validation and settings management using Python type annotations.
    - [sqlalchemy](https://www.sqlalchemy.org/): SQL toolkit and Object-Relational Mapping (ORM) library.
    - [sqlmodel](https://sqlmodel.tiangolo.com/): SQL databases in Python, designed to be compatible with FastAPI.
    - `app.main`: Main application module containing the database session.
    - `.models`: Module containing the Register model.
    - `.schemas`: Module containing the response schemas (`AnimalResponse`, `AnimalUpdate`).
"""

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.db import DbSession

from .models import Register
from .schemas import AnimalCreate, AnimalResponse, AnimalUpdate

api_router = APIRouter(
    prefix="/animales",
    tags=["Animales"],
    responses={404: {"description": "Not found"}},
)


@api_router.get("/", tags=["Animales"])
def animals_list(
    db: DbSession,
) -> list[Register]:
    """Obtiene la lista de todos los animales registrados.

    Este endpoint devuelve todos los animales registrados en la aplicación
    sin aplicar ningún filtro.

    Args:
        db (DbSession): Sesión de base de datos inyectada por FastAPI.

    Returns:
        list[Register]: Una lista con todos los registros de animales.

    """
    return db.exec(select(Register)).all()


@api_router.post("/", tags=["Animales"], status_code=status.HTTP_201_CREATED)
async def create_animal(
    animal: AnimalCreate,
    db: DbSession,
) -> AnimalResponse:
    """Registra un nuevo animal en la base de datos.

    Este endpoint valida y registra un nuevo animal en la aplicación,
    asignándole un ID único automáticamente.

    Args:
        animal (AnimalCreate): Los detalles del animal a registrar.
        db (DbSession): Sesión de base de datos inyectada por FastAPI.

    Returns:
        AnimalResponse: La respuesta que contiene los detalles del animal registrado,
                       incluyendo su ID y fecha de creación.

    """
    db_animal = Register(**animal.dict())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return AnimalResponse.from_orm(db_animal)


@api_router.get("/{animal_id}", tags=["Animales"])
async def get_animal(
    animal_id: int,
    db: DbSession,
) -> AnimalResponse:
    """Obtiene los detalles de un animal específico.

    Este endpoint recupera la información completa de un animal
    a partir de su ID único.

    Args:
        animal_id (int): El ID del animal a consultar.
        db (DbSession): Sesión de base de datos inyectada por FastAPI.

    Returns:
        AnimalResponse: La respuesta que contiene los detalles del animal.

    Raises:
        HTTPException: Si el animal no se encuentra, se lanza un error 404 Not Found.

    """
    animal = db.get(Register, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return AnimalResponse.from_orm(animal)


@api_router.put("/{animal_id}", tags=["Animales"])
async def update_animal(
    animal_id: int,
    animal_update: AnimalUpdate,
    db: DbSession,
) -> AnimalResponse:
    """Actualiza los detalles de un animal específico.

    Este endpoint permite modificar parcial o totalmente la información
    de un animal existente a partir de su ID.

    Args:
        animal_id (int): El ID del animal a actualizar.
        animal_update (AnimalUpdate): Los datos actualizados del animal.
        db (DbSession): Sesión de base de datos inyectada por FastAPI.

    Returns:
        AnimalResponse: La respuesta que contiene los detalles actualizados del animal.

    Raises:
        HTTPException: Si el animal no se encuentra, se lanza un error 404 Not Found.

    """
    animal = db.get(Register, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    for key, value in animal_update.dict(exclude_unset=True).items():
        setattr(animal, key, value)

    db.add(animal)
    db.commit()
    db.refresh(animal)
    return AnimalResponse.from_orm(animal)


@api_router.delete("/{animal_id}", tags=["Animales"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_animal(
    animal_id: int,
    db: DbSession,
):
    """Elimina el registro de un animal específico.

    Este endpoint elimina permanentemente un registro de animal
    de la base de datos a partir de su ID.

    Args:
        animal_id (int): El ID del animal a eliminar.
        db (DbSession): Sesión de base de datos inyectada por FastAPI.

    Raises:
        HTTPException: Si el animal no se encuentra, se lanza un error 404 Not Found.

    """
    animal = db.get(Register, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    db.delete(animal)
    db.commit()
    return {"detail": "Animal eliminado correctamente"}
