"""API routes for managing products in the application.

Routes:
    - POST /productos: Create a new product.
    - GET /productos: Retrieve the list of all products.
    - GET /productos/{producto_id}: Retrieve a product by its ID.
    - PUT /productos/{producto_id}: Update an existing product.
    - DELETE /productos/{producto_id}: Delete a product by its ID.

Functions:
    - create_producto: Create a new product.
    - get_productos: Retrieve the list of all products.
    - get_producto: Retrieve a product by its ID.
    - update_producto: Update an existing product.
    - delete_producto: Delete a product by its ID.

Dependencies:
    - [fastapi](https://fastapi.tiangolo.com/): FastAPI framework for building APIs.
    - [pydantic](https://docs.pydantic.dev/): Data validation and settings management using Python type annotations.
    - [sqlalchemy](https://www.sqlalchemy.org/): SQL toolkit and Object-Relational Mapping (ORM) library.
    - [sqlmodel](https://sqlmodel.tiangolo.com/): SQL databases in Python, designed to be compatible with FastAPI.
    - app.main: Main application module containing the database session.
    - .models: Module containing the Producto model.
"""

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.db import DbSession
from app.proyectos.dramos.schemas import ProductoBase, ProductoCreate, ProductoRead  # noqa: F401

from .models import Producto

api_router = APIRouter(
    prefix="/productos",
    tags=["Productos"],
    responses={404: {"description": "Not found"}},
)


@api_router.post("/", tags=["Productos"], status_code=status.HTTP_201_CREATED)
def create_producto(producto: Producto, db: DbSession) -> Producto:
    """Crear un nuevo producto en la base de datos.

    Args:
        producto (Producto): Datos del producto a crear.
        db (DbSession): Sesión de base de datos.

    Returns:
        Producto: El producto creado.

    """
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


@api_router.get("/", tags=["Productos"])
def get_productos(db: DbSession) -> list[Producto]: # type: ignore
    """Obtener la lista de todos los productos.

    Args:
        db (DbSession): Sesión de base de datos.

    Returns:
        list[Producto]: Lista de productos en la base de datos.

    """
    return db.exec(select(Producto)).all()


@api_router.get("/{producto_id}", tags=["Productos"])
def get_producto(producto_id: int, db: DbSession) -> Producto: # type: ignore
    """Obtener un producto por su ID.

    Args:
        producto_id (int): ID del producto.
        db (DbSession): Sesión de base de datos.

    Returns:
        Producto: El producto correspondiente al ID.

    """
    producto = db.get(Producto, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )


@api_router.put("/{producto_id}", tags=["Productos"])
def update_producto(producto_id: int, producto_data: Producto, db: DbSession) -> Producto: # type: ignore
    """Actualizar un producto existente.

    Args:
        producto_id (int): ID del producto a actualizar.
        producto_data (Producto): Datos actualizados del producto.
        db (DbSession): Sesión de base de datos.

    Returns:
        Producto: El producto actualizado.

    """
    producto = db.get(Producto, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado",
        )
    for key, value in producto_data.dict(exclude_unset=True).items():
        setattr(producto, key, value)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


@api_router.delete(
    "/{producto_id}", tags=["Productos"], status_code=status.HTTP_204_NO_CONTENT,
)
def delete_producto(producto_id: int, db: DbSession):
    """Eliminar un producto por su ID.

    Args:
        producto_id (int): ID del producto a eliminar.
        db (DbSession): Sesión de base de datos.

    """
    producto = db.get(Producto, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado",
        )
    db.delete(producto)
    db.commit()