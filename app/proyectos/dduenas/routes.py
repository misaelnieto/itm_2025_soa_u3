"""API routes for managing books in the application.

Routes:
    - `POST /estudiantes`: Create a new student.
    - `GET /estudiantes`: Retrieve the list of all students.
    - `GET /estudiantes/{estudiante_id}`: Retrieve a student by its ID.
    - `PUT /estudiantes/{estudiante_id}`: Update an existing student.
    - `DELETE /estudiantes/{estudiante_id}`: Delete a book by its ID.

Functions:
    - `create_estudiante`: Create a new student.
    - `get_estudiante`: Retrieve the list of all students.
    - `get_estudiante`: Retrieve a student by its ID.
    - `update_estudiante`: Update an existing student.
    - `delete_estudiante`: Delete a student by its ID.

Dependencies:
    - [fastapi](https://fastapi.tiangolo.com/): FastAPI framework for building APIs.
    - [pydantic](https://docs.pydantic.dev/): Data validation and settings management using Python type annotations.
    - [sqlalchemy](https://www.sqlalchemy.org/): SQL toolkit and Object-Relational Mapping (ORM) library.
    - [sqlmodel](https://sqlmodel.tiangolo.com/): SQL databases in Python, designed to be compatible with FastAPI.
    - `app.main`: Main application module containing the database session.
    - `.models`: Module containing the Transaction model.
"""


from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.db import DbSession

from .models import Transaction
from .schemas import Eliminado

api_router = APIRouter(
    prefix="/estudiantes",
    tags=["Estudiantes"],
    responses={404: {"description": "Not found"}},
)


@api_router.post("/", tags=["Estudiantes"], status_code=status.HTTP_201_CREATED)
def create_estudiantes(estudiante: Transaction, db: DbSession) -> Transaction:  
    """Crear un nuevo estudiante en la base de datos.

    Args:
        estudiante (Transaction): Datos del estudiante a crear.
        db (DbSession): Sesión de base de datos.

    Returns:
        Transaction: El estudiante ha sido creado.

    """
    db.add(estudiante)
    db.commit()
    db.refresh(estudiante)
    return estudiante


@api_router.get("/", tags=["Estudiantes"])
def get_estudiantes(db: DbSession) -> list[Transaction]:
    """Obtener la lista de todos los estudiantes.

    Args:
        db (DbSession): Sesión de base de datos.

    Returns:
        list[Transaction]: Lista de estudiantes en la base de datos.

    """
    return db.exec(select(Transaction)).all()


@api_router.get("/{Estudiante_id}", tags=["Estudiantes"])
def get_estudiante(Estudiante_id: int, db: DbSession) -> Transaction:
    """Obtener un estudiante por su ID.

    Args:
        Estudiante_id (int): ID del estudiante.
        db (DbSession): Sesión de base de datos.

    Returns:
        Transaction: El estudiante correspondiente al ID.

    """
    estudiante = db.get(Transaction, Estudiante_id)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado.",
        )
    return estudiante


@api_router.put("/{estudiante_id}", tags=["Estudiantes"])
def update_estudiante(estudiante_id: int, estudiante_data: Transaction, db: DbSession) -> Transaction:
    """Actualizar un estudiante existente.

    Args:
        estudiante_id (int): ID del estudiante a actualizar.
        estudiante_data (Transaction): Datos actualizados del estudiante.
        db (DbSession): Sesión de base de datos.

    Returns:
        Transaction: El estudiante actualizado.

    """
    estudiante = db.get(Transaction, estudiante_id)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado",
        )
    for key, value in estudiante_data.dict(exclude_unset=True).items():
        setattr(estudiante, key, value)
    db.add(estudiante)
    db.commit()
    db.refresh(estudiante)
    return estudiante


@api_router.delete(
    "/{estudiante_id}", tags=["Estudiantes"], status_code=status.HTTP_204_NO_CONTENT,
)
def delete_estudiante(estudiante_id: int, db: DbSession):
    """Eliminar un estudiante por su ID.

    Args:
        estudiante_id (int): ID del estudiante a eliminar.
        db (DbSession): Sesión de base de datos.

    """
    estudiante = db.get(Transaction, estudiante_id)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado",
        )
    db.delete(estudiante)
    db.commit()
    return Eliminado(message="Estudiante eliminado correctamente.")
