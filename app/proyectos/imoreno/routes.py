"""The module defines the API routes for the hotel management system.

It provides endpoints for managing hotel operations, including client management
and operation listing functionality using FastAPI.
"""

from fastapi import APIRouter, HTTPException
from sqlalchemy import func
from sqlmodel import select

from app.db import DbSession

from .models import Operation
from .schemas import ClientUpdate, OperationResponse, OperationResult, OperationType

api_router = APIRouter(
    prefix="/hotel",
    tags=["Hotel"],
    responses={404: {"description": "Not found"}},
)

async def getTotalClients(db: DbSession) -> int:
    """Compute the total clients by counting the clients in the database.
    
    Args:
        db (Session): The database session used to execute the query.

    Returns:
    int: The total clients computed from the count of all clients. 
    Returns 0 if there are no clients.

    """
    result = db.exec(select(func.coalesce(func.count(Operation.client_id), 0)))
    return result.one_or_none()

async def search_client_by_name(
        db: DbSession,
        first_name: str | None = None,
        middle_name: str | None = None,
        last_name: str | None = None,
        ) -> Operation | None:
    """Search for a client in the database by their full name.

    Args:
        db (Session): The database session used to execute the query.
        first_name (str): The first name of the client.
        middle_name (str): The middle name of the client.
        last_name (str): The last name of the client.

    Returns:
        Operation | None: The client object if found, otherwise None.

    """
    conditions = []
    if first_name != "":
        conditions.append(Operation.first_name == first_name)
    if middle_name != "":
        conditions.append(Operation.middle_name == middle_name)
    if last_name != "":
        conditions.append(Operation.last_name == last_name)
    
    statement = select(Operation).where(*conditions)
    return db.exec(statement).first()

@api_router.get("/operations", tags=["hotel"])
def operations_list(
    db: DbSession,
) -> list[Operation]:
    """Retrieve the list of all operations in **HotelOperations**.

    This endpoint returns all operations recorded in the hotel application.
    - **Returns**: `list[Operation]`: A list of all operations in the database.
    """
    return db.exec(select(Operation)).all()

@api_router.post("/operations/{opType}", status_code=201)
def add_client(client_update: ClientUpdate, db: DbSession, opType: OperationType):
    """Add a new client to the hotel database.

    Args:
        client_update (ClientUpdate): The new client's data.
        db (DbSession): The database session used to execute the query.
        opType (OperationType): The type of operation to perform.

    Returns:
        OperationResponse: The result of the add operation.

    """
    if opType != OperationType.add:
        raise HTTPException(status_code=400, detail="Invalid operation type")
    client = Operation(**client_update.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)

    return OperationResponse(
        result=OperationResult.success if client else OperationResult.failed,
        previous_data=None,
        data=client.model_dump(),
    )

@api_router.put("/operations/{opType}", status_code=200)
async def update_client(client_update: ClientUpdate, db: DbSession, opType: OperationType) -> OperationResponse:
    """Update a client's information in the hotel database by searching for their name.

    Args:
        client_update (ClientUpdate): The new data for the client.
        db (DbSession): The database session used to execute the query.
        opType (OperationType): The type of operation to perform.

    Returns:
        OperationResponse: The result of the update operation.

    """
    if opType != OperationType.update:
        raise HTTPException(status_code=400, detail="Invalid operation type")
    
    # Buscar cliente por nombre
    client = await search_client_by_name(
        db,
        first_name = client_update.first_name,
        middle_name = client_update.middle_name,
        last_name = client_update.last_name,
    )

    old_data = client.model_dump() if client else None
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Actualizar los datos del cliente
    update_data = client_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(client, key, value)
    
    db.add(client)
    db.commit()
    db.refresh(client)

    return OperationResponse(
        result = OperationResult.success if client else OperationResult.failed,
        previous_data = old_data,
        data=client.model_dump(),
    )

@api_router.delete("/operations/{opType}", status_code=200)
async def delete_client(opType: OperationType,
    db: DbSession,
    first_name: str | None = None,
    middle_name: str | None = None,
    last_name: str | None = None,
) -> OperationResponse:
    """Delete a client from the hotel database.

    Args:
        opType (OperationType): The type of operation to perform.
        db (DbSession): The database session used to execute the query.
        first_name (str, optional): The client's first name. Defaults to None.
        middle_name (str, optional): The client's middle name. Defaults to None.
        last_name (str, optional): The client's last name. Defaults to None


    Returns:
        OperationResponse: The result of the delete operation.

    """
    if opType != OperationType.delete:
        raise HTTPException(status_code=400, detail="Invalid operation type")
    
    client = await search_client_by_name(
        db,
        first_name = first_name,
        middle_name = middle_name,
        last_name = last_name,
    )
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()

    return OperationResponse(
        result=OperationResult.success if client else OperationResult.failed,
        previous_data=client.model_dump() if client else None,
        data=None,
    )

@api_router.get("/operations/{opType}", status_code=200)
async def search_client(
    opType: OperationType,
    db: DbSession,
    first_name: str | None = None,
    middle_name: str | None = None,
    last_name: str | None = None,
) -> OperationResponse:
    """Search  for a client in the hotel database by their name or get list of clients.

    Args:
        opType (OperationType): The type of operation to perform. Either Operation.search or Operation.list.
        first_name (str, optional): The client's first name. Defaults to None.
        middle_name (str, optional): The client's middle name. Defaults to None.
        last_name (str, optional): The client's last name. Defaults to None.
        db (DbSession): The database session used to execute the query.

    Returns:
        OperationResponse: The result of the search operation.

    """
    if opType not in [OperationType.search, OperationType.list]:
        raise HTTPException(status_code=400, detail="Invalid operation type")

    
    if opType == OperationType.list:
        clientsList = await getTotalClients(db)
        return OperationResponse(
            result=OperationResult.success,
            previous_data=None,
            data=clientsList.model_dump() if clientsList else None,
        )
    client = await search_client_by_name(
        db,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
    )

    return OperationResponse(
        result=OperationResult.success if client else OperationResult.failed,
        previous_data=None,
        data=client.model_dump() if client else None,
    )