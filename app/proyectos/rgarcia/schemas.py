"""Esquemas de validación de datos."""
from enum import StrEnum

from pydantic import BaseModel


class RecipeResult(StrEnum):
    """Defines the result of the opeartion made with a recipe."""

    non_existant = "non_existant"
    failed = "failed"
    successful = "successful"

class RecipeResponse(BaseModel):
    """Represents the result of a recipe operation."""

    result: RecipeResult
    """The result of this operation"""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "result": "successful",  # Example where the operation is successful
                },
                {
                    "result": "failed",  # Example where the operation failed
                },
                {
                    "result": "non_existant",  # Example where the recipe does not exist
                },
            ],
        },
    }
