"""API routes for managing books in the application.

Routes:
    - `POST /libros`: Create a new book.
    - `GET /libros`: Retrieve the list of all books.
    - `GET /libros/{libro_id}`: Retrieve a book by its ID.
    - `PUT /libros/{libro_id}`: Update an existing book.
    - `DELETE /libros/{libro_id}`: Delete a book by its ID.

Functions:
    - `create_libro`: Create a new book.
    - `get_libros`: Retrieve the list of all books.
    - `get_libro`: Retrieve a book by its ID.
    - `update_libro`: Update an existing book.
    - `delete_libro`: Delete a book by its ID.

Dependencies:
    - [fastapi](https://fastapi.tiangolo.com/): FastAPI framework for building APIs.
    - [pydantic](https://docs.pydantic.dev/): Data validation and settings management using Python type annotations.
    - [sqlalchemy](https://www.sqlalchemy.org/): SQL toolkit and Object-Relational Mapping (ORM) library.
    - [sqlmodel](https://sqlmodel.tiangolo.com/): SQL databases in Python, designed to be compatible with FastAPI.
    - `app.main`: Main application module containing the database session.
    - `.models`: Module containing the Book model.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.db import DbSession

from .models import Book
from .schemas import BookCreate, BookRead

api_router = APIRouter(
    prefix="/libros",
    tags=["Libros"],
    responses={404: {"description": "Not found"}},
)


@api_router.post(
    "/", tags=["Libros"], status_code=status.HTTP_201_CREATED, response_model=BookRead
)
def create_libro(libro: BookCreate, db: DbSession) -> BookRead:
    """Crear un nuevo libro en la base de datos.

    Args:
        libro (BookCreate): Datos del libro a crear.
        db (DbSession): Sesión de base de datos.

    Returns:
        BookRead: El libro creado.

    """
    new_libro = Book(**libro.dict())
    db.add(new_libro)
    db.commit()
    db.refresh(new_libro)
    return new_libro


@api_router.get("/", tags=["Libros"], response_model=list[BookRead])
def get_libros(db: DbSession) -> list[BookRead]:
    """Obtener la lista de todos los libros.

    Args:
        db (DbSession): Sesión de base de datos.

    Returns:
        list[BookRead]: Lista de libros en la base de datos.

    """
    return db.exec(select(Book)).all()


@api_router.get("/{libro_id}", tags=["Libros"], response_model=BookRead)
def get_libro(libro_id: int, db: DbSession) -> BookRead:
    """Obtener un libro por su ID.

    Args:
        libro_id (int): ID del libro.
        db (DbSession): Sesión de base de datos.

    Returns:
        BookRead: El libro correspondiente al ID.

    """
    libro = db.get(Book, libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado.",
        )
    return libro


@api_router.put("/{libro_id}", tags=["Libros"], response_model=BookRead)
def update_libro(libro_id: int, libro_data: BookCreate, db: DbSession) -> BookRead:
    """Actualizar un libro existente.

    Args:
        libro_id (int): ID del libro a actualizar.
        libro_data (BookCreate): Datos actualizados del libro.
        db (DbSession): Sesión de base de datos.

    Returns:
        BookRead: El libro actualizado.

    """
    libro = db.get(Book, libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado",
        )
    for key, value in libro_data.dict(exclude_unset=True).items():
        setattr(libro, key, value)
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


@api_router.delete(
    "/{libro_id}",
    tags=["Libros"],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_libro(libro_id: int, db: DbSession):
    """Eliminar un libro por su ID.

    Args:
        libro_id (int): ID del libro a eliminar.
        db (DbSession): Sesión de base de datos.

    """
    libro = db.get(Book, libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado",
        )
    db.delete(libro)
    db.commit()
