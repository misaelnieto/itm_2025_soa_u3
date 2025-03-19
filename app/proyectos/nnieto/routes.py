"""API routes for managing transactions in the "alcancia" (piggy bank) application.

Routes:
    - GET /alcancia/transactions: Retrieve the list of all transactions.
    - PUT /alcancia/transaction/{txn_type}/{quantity}: Create a new transaction (deposit or withdraw).
    - GET /alcancia/saldo/{dsds}: Calculate the current balance (deprecated).
    - POST /alcancia/deposito: Make a deposit (deprecated).
    - POST /alcancia/retiro: Make a withdrawal (deprecated).
    - GET /alcancia/movimientos: Retrieve the list of all transactions (deprecated).
Functions:
    - _compute_balance(db: Session) -> int: Compute the balance by summing up the amounts of all transactions in the database.
    - transactions_list(db: DbSession) -> list[Transaction]: Retrieve the list of all transactions.
    - create_transaction(txn_type: TransactionType, quantity: PositiveInt, db: DbSession) -> TransactionResponse: Create a new transaction.
    - saldo(db: DbSession) -> RespuestaSaldo: Calculate the current balance (deprecated).
    - deposito(cantidad: int, db: DbSession) -> TransactionResponse: Make a deposit (deprecated).
    - retiro(cantidad: int, db: DbSession) -> TransactionResponse: Make a withdrawal (deprecated).
    - movimientos(db: DbSession) -> list[Transaction]: Retrieve the list of all transactions (deprecated).
Dependencies:
    - fastapi: FastAPI framework for building APIs.
    - pydantic: Data validation and settings management using Python type annotations.
    - sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library.
    - sqlmodel: SQL databases in Python, designed to be compatible with FastAPI.
    - app.main: Main application module containing the database session.
    - .models: Module containing the Transaction model.
    - .schemas: Module containing the response schemas (RespuestaSaldo, TransactionResponse, TransactionResult, TransactionType).
Author:
    - Noe Nieto <nnieto@noenieto.com>
License:
    - MIT License
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt, Field
from sqlalchemy import func
from sqlmodel import select
from typing_extensions import Doc

from app.db import DbSession

from .models import Transaction
from .schemas import TransactionResponse, TransactionResult, TransactionType


async def compute_balance(db: DbSession) -> int:
    """Compute the balance by summing up the amounts of all transactions in the database.

    Args:
        db (Session): The database session used to execute the query.

    Returns:
        int: The total balance computed from the sum of all transaction amounts. 
             Returns 0 if there are no transactions.

    """
    result = db.exec(select(func.coalesce(func.sum(Transaction.amount), 0)))
    return result.one_or_none()


api_router = APIRouter(
    prefix="/alcancia",
    tags=["Alcancia"],
    responses={404: {"description": "Not found"}},
)


@api_router.get("/transactions", tags=["Alcancia"])
def transactions_list(
    db: DbSession,
) -> list[Transaction]:
    """Retrieve the list of all transactions in **Alcancia**.

    This endpoint returns all transactions recorded in the Alcancia application.
    
    - **Returns**: `list[Transaction]`: A list of all transactions in the database.
    """
    return db.exec(select(Transaction)).all()


@api_router.put("/transaction/{txn_type}/{quantity}", tags=["Alcancia"], status_code=status.HTTP_201_CREATED)
async def create_transaction(
    txn_type: TransactionType,
    quantity: PositiveInt,
    db: DbSession,
    balance: Annotated[int, Depends(compute_balance)],
) -> TransactionResponse:
    """Create a new transaction (`deposit` or `withdraw`) in **Alcancia**.

    This endpoint creates a new transaction in the **Alcancia** application. It can
    handle both deposit and withdrawal transactions. If the transaction type is
    `withdraw` and the quantity exceeds the current balance, the transaction is
    rejected.

    **Args:**
    - `txn_type` (`TransactionType`): The type of transaction (`"deposit"` or `"withdraw"`).
    - `quantity` (`PositiveInt`): The amount for the transaction. *Important*:
       Provide a positive integer representing cents, not units.

    **Returns:**
    - `TransactionResponse`: The response containing the result of the transaction,
      the previous balance, and the new balance.

    **Raises:**
    - `HTTPException`: If the transaction is a withdrawal and the quantity exceeds
      the current balance, a 403 Forbidden error is raised with a rejection response.
    """
    if txn_type == TransactionType.withdraw and quantity > balance:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=TransactionResponse(
                result=TransactionResult.rejected,
                previous_balance=balance,
                balance=balance,
            ).model_dump(),
        )
    op = 1 if txn_type== TransactionType.deposit else -1
    db.add(Transaction(amount=quantity * op))
    db.commit()
    new_balance = await compute_balance(db)
    return TransactionResponse(
        result=TransactionResult.settled,
        previous_balance=balance, balance=new_balance,
    )


