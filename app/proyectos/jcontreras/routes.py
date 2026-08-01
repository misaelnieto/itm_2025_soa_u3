"""API routes for managing sales in the application.

Routes:
    - POST /ventas: Create a new sale.
    - GET /ventas: Retrieve the list of all sales.
    - GET /ventas/{venta_id}: Retrieve a sale by its ID.
    - PUT /ventas/{venta_id}: Update an existing sale.
    - DELETE /ventas/{venta_id}: Delete a sale by its ID.

Functions:
    - create_venta: Create a new sale.
    - get_ventas: Retrieve the list of all sales.
    - get_venta: Retrieve a sale by its ID.
    - update_venta: Update an existing sale.
    - delete_venta: Delete a sale by its ID.

Dependencies:
    - [fastapi](https://fastapi.tiangolo.com/): FastAPI framework for building APIs.
    - [pydantic](https://docs.pydantic.dev/): Data validation and settings management using Python type annotations.
    - [sqlalchemy](https://www.sqlalchemy.org/): SQL toolkit and Object-Relational Mapping (ORM) library.
    - [sqlmodel](https://sqlmodel.tiangolo.com/): SQL databases in Python, designed to be compatible with FastAPI.
    - app.main: Main application module containing the database session.
    - .models: Module containing the Sale model.
"""


from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.db import DbSession

from .models import Sale
from .schemas import SaleCreate

api_router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"],
    responses={404: {"description": "Not found"}},
)



@api_router.post("/", status_code=status.HTTP_201_CREATED)
def create_venta(venta: SaleCreate, db: DbSession) -> Sale:
    """Crear una nueva venta en la base de datos."""
    # Crear una instancia de tipo Sale
    new_venta = Sale(cliente=venta.cliente, producto=venta.producto, cantidad=venta.cantidad, precio=venta.precio)
    db.add(new_venta)
    db.commit()
    db.refresh(new_venta)
    return new_venta

@api_router.get("/")
def get_ventas(db: DbSession) -> list[Sale]:
    """Obtener la lista de todas las ventas."""
    return db.exec(select(Sale)).all()

@api_router.get("/{venta_id}")
def get_venta(venta_id: int, db: DbSession) -> Sale:
    """Obtener una venta por su ID."""
    new_venta = db.exec(select(Sale).where(Sale.id == venta_id)).first()
    if not new_venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada.")
    return new_venta

@api_router.put("/{venta_id}")
def update_venta(venta_id: int, venta_data: SaleCreate, db: DbSession) -> Sale:
    """Actualizar una venta existente."""
    new_venta = db.exec(select(Sale).where(Sale.id == venta_id)).first()
    if not new_venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada.")
    
    for key, value in venta_data.dict(exclude_unset=True).items():
        setattr(new_venta, key, value)
    
    db.add(new_venta)
    db.commit()
    db.refresh(new_venta)
    return new_venta

@api_router.delete("/{venta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venta(venta_id: int, db: DbSession):
    """Eliminar una venta por su ID."""
    new_venta = db.exec(select(Sale).where(Sale.id == venta_id)).first()
    if not new_venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada.")
    
    db.delete(new_venta)
    db.commit()
