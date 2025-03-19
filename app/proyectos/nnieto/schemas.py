"""Esquemas de validación de datos."""
from enum import StrEnum

from pydantic import BaseModel


class TransactionType(StrEnum):
    """Defines the transaction type. Only two types at the moment."""

    deposit = "deposit"
    withdraw = "withdraw"


class TransactionResult(StrEnum):
    """The transaction result."""

    settled = "settled"
    failed = "failed"
    rejected = "rejected"


class TransactionResponse(BaseModel):
    """Represents the result of a transaction."""

    result: TransactionResult
    """The result of this transaction"""
    previous_balance: int|None
    """The balance before the transaction takes place"""
    balance: int|None
    """The balance after the transaction takes place"""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "result": "settled",
                    "previous_balance": 5000,
                    "balance": 5500,
                },
                {
                    "result": "settled",
                    "previous_balance": 5000,
                    "balance": 4500,
                },
                {
                    "result": "rejected",
                    "previous_balance": 5000,
                    "balance": 5500,
                },
            ],
        },
    }
