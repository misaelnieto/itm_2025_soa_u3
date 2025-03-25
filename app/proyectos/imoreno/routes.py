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
    result = db.exec(select(func.coalesce(func.count(Operation.client), 0)))
    return result.one_or_none()

@api_router.get("/operations", tags=["HotelOperations"])
def operations_list(
    db: DbSession,
) -> list[Operation]:
    """Retrieve the list of all operations in **Alcancia**.

    This endpoint returns all operations recorded in the Alcancia application.
    - **Returns**: `list[Operation]`: A list of all operations in the database.
    """
    return db.exec(select(Operation)).all()

@api_router.put("/operations/{opType}/{client_id}")
def update_client(client_id: int, client_update: ClientUpdate, db: DbSession, opType: OperationType) -> OperationResponse:
    """Update a client's information in the hotel database.

    Args:
        client_id (int): The ID of the client to update.
        client_update (ClientUpdate): The new data for the client.
        db (DbSession): The database session used to execute the query.
        opType (OperationType): The type of operation to perform.

    Returns:
        OperationResponse: The result of the update operation.

    """
    if opType == OperationType.update:
        client = db.get(Operation, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        update_data = client_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(client, key, value)

        db.add(client)
        db.commit()
        db.refresh(client)

    return OperationResponse(
        result=OperationResult.success,
        previous_data=None,
        data=client.model_dump(),
    )