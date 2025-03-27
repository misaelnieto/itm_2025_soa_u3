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

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.db import DbSession

from .models import Register
from .schemas import AnimalResponse, AnimalUpdate, AnimalCreate

api_router = APIRouter(
    prefix="/animales",
    tags=["Animales"],
    responses={404: {"description": "Not found"}},
)


@api_router.get("/", tags=["Animales"])
def animals_list(
    db: DbSession,
) -> list[Register]:
    """Retrieve the list of all registered animals.

    This endpoint returns all animals registered in the application.
    
    - **Returns**: `list[Register]`: A list of all registered animals.
    """
    return db.exec(select(Register)).all()


@api_router.post("/", tags=["Animales"], status_code=status.HTTP_201_CREATED)
async def create_animal(
    animal: AnimalCreate,
    db: DbSession,
) -> AnimalResponse:
    """Register a new animal.

    This endpoint registers a new animal in the application.

    **Args:**
    - `animal` (`AnimalCreate`): The details of the animal to be registered.

    **Returns:**
    - `AnimalResponse`: The response containing the registered animal details.
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
    """Retrieve details of a specific animal.

    This endpoint retrieves the details of a specific animal by its ID.

    **Args:**
    - `animal_id` (`int`): The ID of the animal to be retrieved.

    **Returns:**
    - `AnimalResponse`: The response containing the animal details.

    **Raises:**
    - `HTTPException`: If the animal is not found, a 404 Not Found error is raised.
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
    """Update details of a specific animal.

    This endpoint updates the details of a specific animal by its ID.

    **Args:**
    - `animal_id` (`int`): The ID of the animal to be updated.
    - `animal_update` (`AnimalUpdate`): The updated details of the animal.

    **Returns:**
    - `AnimalResponse`: The response containing the updated animal details.

    **Raises:**
    - `HTTPException`: If the animal is not found, a 404 Not Found error is raised.
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
    """Delete a specific animal registration.

    This endpoint deletes a specific animal registration by its ID.

    **Args:**
    - `animal_id` (`int`): The ID of the animal to be deleted.

    **Raises:**
    - `HTTPException`: If the animal is not found, a 404 Not Found error is raised.
    """
    animal = db.get(Register, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    db.delete(animal)
    db.commit()
    return {"detail": "Animal deleted successfully"}