"""API routes for managing the recipes in "receta" application.

Routes:
    - `GET /recetas/recetas`: Retrieve the list of all recipes.

Functions:
    - `recipes_list`: Retrieve the list of all recipes.
    - `create_transaction`: Create a new transaction (Deposit/Withdraw)

Dependencies:
    - [fastapi](https://fastapi.tiangolo.com/): FastAPI framework for building APIs.
    - [pydantic](https://docs.pydantic.dev/): Data validation and settings management using Python type annotations.
    - [sqlalchemy](https://www.sqlalchemy.org/): SQL toolkit and Object-Relational Mapping (ORM) library.
    - [sqlmodel](https://sqlmodel.tiangolo.com/): SQL databases in Python, designed to be compatible with FastAPI.
    - `app.main`: Main application module containing the database session.
    - `.models`: Module containing the Recipe model.
    - `.schemas`: Module containing the response schemas (`TransactionResponse`, `TransactionResult`, Transaction`Type).
"""

from fastapi import APIRouter, status
from sqlmodel import select

from app.db import DbSession
from app.proyectos.rgarcia.schemas import RecipeResponse, RecipeResult

from .models import Receta

api_router = APIRouter(
    prefix="/recetas",
    tags=["Recetas"],
    responses={404: {"description": "Not found"}},
)

@api_router.get("/todas", tags=["Recetas"])
def recipes_list(
    db: DbSession,
) -> list[Receta]:
    """Retrieve the list of all recipees in **Recetas**.

    This endpoint returns all recipes recorded in the Recetas application.
    
    - **Returns**: `list[Receta]`: A list of all recipes in the database.
    """
    return db.exec(select(Receta)).all()


@api_router.get("/receta", tags=["Recetas"], status_code=status.HTTP_200_OK)
async def get_receta(
    receta_id: int,  
    db: DbSession,  
):
    """Get the existent recipe by its id."""
    # Retrieve the existant recipe
    receta_db = db.exec(select(Receta).where(Receta.id == receta_id)).first()

    # If the recipe does not exist, return a non_existant response
    if not receta_db:
        return RecipeResponse(result=RecipeResult.non_existant)
    
    return receta_db


@api_router.post("/alta", tags=["Recetas"], status_code=status.HTTP_201_CREATED)
async def upload_receta(
    receta: Receta,
    db: DbSession,
):
    """Upload a new receta and its ingredientes."""
    receta_db = Receta(
        nombre=receta.nombre,
        descripcion=receta.descripcion,
        min_preparacion=receta.min_preparacion,
        ingredientes=receta.ingredientes,
        metodo_preparacion=receta.metodo_preparacion,
    )

    db.add(receta_db)
    db.commit()

    return RecipeResponse(result=RecipeResult.successful)


@api_router.put("/modificar", tags=["Recetas"], status_code=status.HTTP_200_OK)
async def update_receta(
    receta: Receta,  
    db: DbSession,   
):
    """Update an existing receta based on the receta.id."""
    # Retrieves the existant recipe
    receta_db = db.exec(select(Receta).where(Receta.id == receta.id)).first()

    # If the recipe does not exist, return a non_existant response
    if not receta_db:
        return RecipeResponse(result=RecipeResult.non_existant)

    receta_db.nombre = receta.nombre
    receta_db.descripcion = receta.descripcion
    receta_db.min_preparacion = receta.min_preparacion
    receta_db.ingredientes = receta.ingredientes
    receta_db.metodo_preparacion = receta.metodo_preparacion

    db.commit()

    return RecipeResponse(result=RecipeResult.successful)


@api_router.delete("/eliminar", tags=["Recetas"], status_code=status.HTTP_200_OK)
async def delete_receta(
    receta_id: int,  
    db: DbSession,  
):
    """Delete an existing receta based on the receta.id."""
    # Retrieve the existant recipe
    receta_db = db.exec(select(Receta).where(Receta.id == receta_id)).first()

    # If the recipe does not exist, return a non_existant response
    if not receta_db:
        return RecipeResponse(result=RecipeResult.non_existant)

    db.delete(receta_db)
    db.commit()

    return RecipeResponse(result=RecipeResult.successful)