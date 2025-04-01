"""API routes for managing courses in the application.

Routes:
    - `POST /cursos`: Create a new course.
    - `GET /cursos`: Retrieve the list of all courses.
    - `GET /cursos/{curso_id}`: Retrieve a course by its ID.
    - `PUT /cursos/{curso_id}`: Update an existing course.
    - `DELETE /cursos/{curso_id}`: Delete a course by its ID.

Functions:
    - `create_curso`: Create a new course.
    - `get_cursos`: Retrieve the list of all courses.
    - `get_curso`: Retrieve a course by its ID.
    - `update_curso`: Update an existing course.
    - `delete_curso`: Delete a course by its ID.

Dependencies:
    - [fastapi](https://fastapi.tiangolo.com/): FastAPI framework for building APIs.
    -[pydantic](https://docs.pydantic.dev/): Data validation and settings management using Python type annotations.
    - [sqlalchemy](https://www.sqlalchemy.org/): SQL toolkit and Object-Relational Mapping (ORM) library.
    - [sqlmodel](https://sqlmodel.tiangolo.com/): SQL databases in Python, designed to be compatible with FastAPI.
    - `app.main`: Main application module containing the database session.
    - `.models`: Module containing the Register model.
    - `.schemas`: Module containing the response schemas (`CourseResponse`, `CourseUpdate`).
"""

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.db import DbSession

from .models import Register
from .schemas import CourseCreate, CourseResponse, CourseUpdate

api_router = APIRouter(
    prefix="/cursos",
    tags=["Cursos"],
    responses={404: {"description": "No encontrado"}},
)

@api_router.post("/", tags=["Cursos"], status_code=status.HTTP_201_CREATED)
async def create_curso(curso: CourseCreate, db: DbSession) -> CourseResponse:
    """Crear un nuevo curso en la base de datos."""
    new_curso = Register(**curso.dict())
    db.add(new_curso)
    db.commit()
    db.refresh(new_curso)
    return CourseResponse.from_orm(new_curso)

@api_router.get("/", tags=["Cursos"])
def get_cursos(db: DbSession) -> list[Register]:
    """Obtener la lista de todos los cursos."""
    return db.exec(select(Register)).all()

@api_router.get("/{curso_id}", tags=["Cursos"])
async def get_curso(curso_id: int, db: DbSession) -> CourseResponse:
    """Obtener un curso por su ID."""
    curso = db.get(Register, curso_id)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado.",
        )
    return CourseResponse.from_orm(curso)

@api_router.put("/{curso_id}", tags=["Cursos"])
async def update_curso(curso_id: int, curso_update: CourseUpdate, db: DbSession) -> CourseResponse:
    """Actualizar un curso existente."""
    curso = db.get(Register, curso_id)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado",
        )
    for key, value in curso_update.dict(exclude_unset=True).items():
        setattr(curso, key, value)
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return CourseResponse.from_orm(curso)

@api_router.delete("/{curso_id}", tags=["Cursos"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: DbSession):
    """Eliminar un curso por su ID."""
    curso = db.get(Register, curso_id)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado",
        )
    db.delete(curso)
    db.commit()
    return {"detail": "Curso eliminado con éxito."}