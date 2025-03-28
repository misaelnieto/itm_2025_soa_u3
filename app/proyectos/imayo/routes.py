"""Rutas de la API para gestionar los eventos en la aplicación.

Rutas:
    - `POST /eventos`: Crear un nuevo evento.
    - `GET /eventos`: Obtener la lista de todos los eventos.
    - `GET /eventos/{event_id}`: Obtener un evento específico por su ID.
    - `PUT /eventos/{event_id}`: Actualizar un evento existente.
    - `DELETE /eventos/{event_id}`: Eliminar un evento específico.

Funciones:
    - `create_event`: Crear un nuevo evento en la base de datos.
    - `get_events`: Obtener todos los eventos almacenados.
    - `get_event`: Obtener un evento específico por su ID.
    - `update_event`: Actualizar los datos de un evento.
    - `delete_event`: Eliminar un evento por su ID.

Dependencias:
    - [FastAPI](https://fastapi.tiangolo.com/): Framework para la construcción de APIs.
    - [SQLModel](https://sqlmodel.tiangolo.com/): ORM para interactuar con bases de datos SQL en Python, compatible con FastAPI.
    - `app.db`: Módulo que maneja la sesión de la base de datos.
    - `.models`: Módulo que contiene el modelo `Event`.
    - `.schemas`: Módulo que contiene los esquemas de respuesta (`EventCreate`, `EventRead`).
"""

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.db import DbSession

from .models import Event
from .schemas import EventCreate, EventRead

api_router = APIRouter(
    prefix="/eventos",
    tags=["Eventos"],
    responses={404: {"description": "No encontrado"}},
)

@api_router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: DbSession) -> Event:
    """Crear un nuevo evento en la base de datos.

    Esta ruta permite crear un evento en la base de datos.

    - **Entrada**:
        - `event` (tipo: `EventCreate`): Datos necesarios para crear el evento.
    - **Salida**:
        - `EventRead`: Detalles del evento creado.
    - **Código de estado**:
        - `201 Created`: Si el evento es creado correctamente.
    """
    db_event = Event.from_orm(event)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@api_router.get("/", response_model=list[EventRead])
def get_events(db: DbSession) -> list[Event]:
    """Obtener la lista de todos los eventos.

    Esta ruta devuelve todos los eventos almacenados en la base de datos.

    - **Entrada**: Ninguna.
    - **Salida**:
        - `list[EventRead]`: Lista de eventos.
    """
    return db.exec(select(Event)).all()

@api_router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: DbSession) -> Event:
    """Obtener un evento por su ID.

    Esta ruta permite obtener un evento específico por su identificador único.

    - **Entrada**:
        - `event_id` (tipo: `int`): ID del evento a consultar.
    - **Salida**:
        - `EventRead`: Detalles del evento solicitado.
    - **Código de estado**:
        - `404 Not Found`: Si no se encuentra el evento.
    """
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado.",
        )
    return event

@api_router.put("/{event_id}", response_model=EventRead)
def update_event(event_id: int, event_data: EventCreate, db: DbSession) -> Event:
    """Actualizar un evento existente.

    Esta ruta permite actualizar los datos de un evento específico.

    - **Entrada**:
        - `event_id` (tipo: `int`): ID del evento a actualizar.
        - `event_data` (tipo: `EventCreate`): Nuevos datos del evento.
    - **Salida**:
        - `EventRead`: Detalles del evento actualizado.
    - **Código de estado**:
        - `404 Not Found`: Si no se encuentra el evento.
    """
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado",
        )
    event_dict = event_data.dict(exclude_unset=True)
    for key, value in event_dict.items():
        setattr(event, key, value)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@api_router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: DbSession):
    """Eliminar un evento por su ID.

    Esta ruta permite eliminar un evento específico por su ID.

    - **Entrada**:
        - `event_id` (tipo: `int`): ID del evento a eliminar.
    - **Salida**: Ninguna.
    - **Código de estado**:
        - `204 No Content`: Si el evento es eliminado correctamente.
        - `404 Not Found`: Si no se encuentra el evento.
    """
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado",
        )
    db.delete(event)
    db.commit()

