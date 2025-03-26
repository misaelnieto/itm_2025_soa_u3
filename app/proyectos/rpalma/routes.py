"""API routes for managing contactos in the "Contactos" application.

Routes:
    - `GET /contactos/agenda`: Retrieve the list of all contactos.
    - `POST /contactos/create`: Create a new contacto in the agenda.
    - `PUT /contactos/edit/{contacto_id}`: Edit an existing contacto by ID.
    - `DELETE /contactos/delete/{contacto_id}`: Delete a contacto by ID.
    - `GET /contactos/search/{nombre}`: Search for contactos by name.

Functions:
    - `agenda_list`: Retrieve the list of all contactos in the agenda.
    - `crear_contacto`: Create a new contacto in the agenda.
    - `editar_contacto`: Edit an existing contacto by ID.
    - `eliminar_contacto`: Delete a contacto by ID.
    - `buscar_contacto`: Search for contactos by name.

Dependencies:
    - [fastapi](https://fastapi.tiangolo.com/): FastAPI framework for building APIs.
    - [pydantic](https://docs.pydantic.dev/): Data validation and settings management using Python type annotations.
    - [sqlalchemy](https://www.sqlalchemy.org/): SQL toolkit and Object-Relational Mapping (ORM) library.
    - [sqlmodel](https://sqlmodel.tiangolo.com/): SQL databases in Python, designed to be compatible with FastAPI.
    - `app.db`: Module containing the database session.
    - `.models`: Module containing the `Agenda` model.
    - `.schemas`: Module containing the response schemas (`ContactoDB`, `ContactoResponse`).
"""
from fastapi import APIRouter, status
from sqlmodel import select

from app.db import DbSession

from .models import Agenda
from .schemas import ContactoDB, ContactoResponse

api_router = APIRouter(
    prefix="/contactos",
    tags=["Contactos"],
    responses={404: {"description": "Not found"}},
)


@api_router.get("/agenda", tags=["Contactos"])
def agenda_list(
    db: DbSession,
) -> list[Agenda]:
    """Retrieve the list of all contactos in **Agenda**.

    This endpoint returns all contactos recorded in the Contactos application.
    
    - **Returns**: `list[Agenda]`: A list of all contactos in the database.
    """
    return db.exec(select(Agenda)).all()

@api_router.post("/create", tags=["Contactos"], status_code=status.HTTP_201_CREATED)
async def crear_contacto(
    contacto: ContactoDB,  # Pydantic schema for validation
    db: DbSession,
) -> ContactoResponse:
    """Create a new contacto in the **Agenda**.

    This endpoint allows you to create a new contacto by providing the required details.

    - **Request Body**: `ContactoDB` schema with `nombre`, `telefono`, and optional `correo`.
    - **Returns**: `ContactoResponse`: The result of the operation and the updated agenda.
    """
    # Create a new Agenda instance from the validated data      
    nuevo_contacto=Agenda(
        nombre = contacto.nombre,
        telefono = contacto.telefono,
        correo = contacto.correo,
    )

    # Add the new contacto to the database
    db.add(nuevo_contacto)
    db.commit()
    db.refresh(nuevo_contacto)  # Refresh to get the updated instance with the ID

    # Retrieve the updated agenda
    agenda_actualizada = db.exec(select(Agenda)).all()

    # Return the response object directly
    return ContactoResponse(
        status="successful",
        message="Contacto created successfully",
        agenda=agenda_actualizada,
    )

@api_router.put("/edit/{contacto_id}", tags=["Contactos"])
async def editar_contacto(
    contacto_id: int,
    contacto: ContactoDB,
    db: DbSession,
) -> ContactoResponse:
    """Edit an existing contacto in the **Agenda**.

    This endpoint allows you to edit an existing contacto by providing the contacto ID and updated details.

    - **Path Parameter**: `contacto_id` - The ID of the contacto to be edited.
    - **Request Body**: `ContactoDB` schema with updated `nombre`, `telefono`, and optional `correo`.
    - **Returns**: `ContactoResponse`: The result of the operation and the updated agenda.
    """
    # Retrieve the existing contacto from the database
    contacto_existente = db.get(Agenda, contacto_id)

    if not contacto_existente:
        return ContactoResponse(
            status="failed",
            message="Contacto not found",
            agenda=None,
        )

    # Update the contacto details
    if contacto.nombre is not None:
        contacto_existente.nombre = contacto.nombre
    if contacto.telefono is not None:
        contacto_existente.telefono = contacto.telefono
    if contacto.correo is not None:
        contacto_existente.correo = contacto.correo

    # Commit the changes to the database
    db.commit()
    db.refresh(contacto_existente)

    # Retrieve the updated agenda
    agenda_actualizada = db.exec(select(Agenda)).all()

    # Return the response object directly
    return ContactoResponse(
        status="successful",
        message="Contacto updated successfully",
        agenda=agenda_actualizada,
    )
        
@api_router.delete("/delete/{contacto_id}", tags=["Contactos"])
async def eliminar_contacto(
    contacto_id: int,
    db: DbSession,
) -> ContactoResponse:
    """Delete a contacto from the **Agenda**.

    This endpoint allows you to delete a contacto by providing the contacto ID.

    - **Path Parameter**: `contacto_id` - The ID of the contacto to be deleted.
    - **Returns**: `ContactoResponse`: The result of the operation and the updated agenda.
    """
    # Retrieve the existing contacto from the database
    contacto_existente = db.get(Agenda, contacto_id)

    if not contacto_existente:
         return ContactoResponse(
        status="failed",
        message="Contacto not found",
        agenda=None,
    )

    # Delete the contacto from the database
    db.delete(contacto_existente)
    db.commit()

    # Retrieve the updated agenda
    agenda_actualizada = db.exec(select(Agenda)).all()
    
    # Return the response object directly
    return ContactoResponse(
        status="successful",
        message="Contacto deleted successfully",
        agenda=agenda_actualizada,
    )

@api_router.get("/search/{nombre}", tags=["Contactos"])
async def buscar_contacto(
    nombre: str,
    db: DbSession,
) -> ContactoResponse:
    """Search for a contacto in the **Agenda** by name.

    This endpoint allows you to search for a contacto by providing the name.

    - **Path Parameter**: `nombre` - The name of the contacto to search for.
    - **Returns**: `ContactoResponse`: The result of the operation and matching results.
    """
    # Search for contactos with the provided name
    contactos = db.exec(select(Agenda).where(Agenda.nombre == nombre)).all()

    if not contactos:
        return ContactoResponse(
        status="failed",
        message="Contacto not found",
        agenda=None,
    )

    return ContactoResponse(
        status="successful",
        message="Found contactos matching the search criteria",
        agenda=contactos,
    )
    