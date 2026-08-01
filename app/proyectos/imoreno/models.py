"""All the database models here."""
from datetime import UTC, datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


def now_utc():
    """Get the current UTC datetime.

    Returns:
        datetime: The current datetime in UTC.

    """
    return datetime.now(UTC)


class Operation(SQLModel, table=True):
    """Model to register operations in the database."""

    __tablename__ = "hotel_operacion"
    client_id: int | None = Field(default=None, primary_key=True, nullable=True)
    first_name: str = Field(title="First Name", nullable=False)
    middle_name: str = Field(title="Middle Name", nullable=False)
    last_name: str = Field(title="Last Name", nullable=False)
    email: EmailStr = Field(title="Email", nullable=True)
    room: int = Field(title="Room Number", nullable=True)
    check_in: datetime = Field(
        title="Checked In at",
        default_factory=now_utc,
        nullable=False,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Isaí",
                    "middle_name": "Moreno",
                    "last_name": "Mendoza",
                    "id": 4,
                    "email": "isaimoreno@outlook.com",
                    "created_at": "2025-03-13T07:48:04.965275",
                },
                {
                    "first_name": "Jane",
                    "middle_name": "Doe",
                    "last_name": "Smith",
                    "id": 5,
                    "email": "janedoe@protonmail.com",
                    "created_at": "2025-03-14T07:05:07.841158",
                },
			],
        },
    }
