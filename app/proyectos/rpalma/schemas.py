"""Esquemas de validación de datos."""
from pydantic import BaseModel, EmailStr, field_validator

from app.proyectos.rpalma.models import Agenda


class ContactoResponse(BaseModel):
    """Represents the result of an operation on Contacto data."""
    
    status: str
    message: str
    agenda: list[Agenda] | None = None  # Agenda is now optional

class ContactoDB(BaseModel):
    """Contacto(BaseModel) is a Pydantic model that represents the schema for creating a Contacto.

    Attributes:
        nombre (str): The name of the individual or entity associated with the Contacto.
        telefono (str): The phone number of the individual or entity. This field is validated to ensure it is in a valid phone number format.
        correo (EmailStr | None): The email address of the individual or entity. This field is optional and can be None.

    Methods:
        validate_telefono(cls, value):
            Validates the phone number format. Ensures the phone number:
            - Contains only digits or starts with a '+' followed by digits.
            - Has at least 10 digits (excluding the '+', if present).
            Raises a ValueError if the phone number contains invalid characters or is too short.
    
    """

    nombre: str
    telefono: str
    correo: EmailStr | None = None

    @field_validator("telefono")
    def validate_telefono(cls, value):
        """Validate the phone number format.

        Ensures the phone number contains only digits and has at least 10 digits.
        
        Raises:
            ValueError: If the phone number contains non-digit characters or is too short.
            
        """
        if value.startswith("+"):  # Allow a leading '+'
            if not value[1:].isdigit():  # Check if the rest of the string contains only digits
                raise ValueError("El telefono solo puede contener números después del '+'.")
        else:
            if not value.isdigit():  # Check if the value contains only digits
                raise ValueError("El telefono solo puede contener números.")
        
        if len(value.replace("+", "")) < 10:  # Check if it has at least 10 digits (excluding '+')
            raise ValueError("El telefono debe tener al menos 10 dígitos.")
        
        return value

