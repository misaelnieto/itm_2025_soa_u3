"""Esquemas de validación de datos para la gestión de cursos."""

from datetime import datetime

from pydantic import BaseModel, field_validator


class CursoBase(BaseModel):
    """Esquema base para un curso."""

    nombre: str
    """Nombre del curso."""
    descripcion: str
    """Descripción del curso."""
    maestro: str
    """Nombre del maestro a cargo del curso."""
    
    @field_validator("nombre", "descripcion", "maestro", mode="before")
    @classmethod
    def validate_not_empty(cls, v):
        """Valida que los campos de texto no estén vacíos."""
        if not v or v.strip() == "":
            raise ValueError("Campo requerido")
        return v

class CourseCreate(CursoBase):
    """Esquema para la creación de un curso."""
    
    class Config:
        """Configuración adicional para el modelo CourseCreate."""
        
        json_schema_extra = {
            "examples": [
                {
                    "nombre": "Introducción a Python",
                    "descripcion": "Curso básico de programación en Python.",
                    "maestro": "Noe Nieto",
                },
                {
                    "nombre": "Introducción a Inteligencia Artificial",
                    "descripcion": "Curso básico de Inteligencia Artificial.",
                    "maestro": "Jaime Olvera",
                },
            ],
        }


class CourseUpdate(BaseModel):
    """Esquema para actualizar un curso existente."""

    nombre: str | None = None
    """Nombre del curso (opcional)"""
    descripcion: str | None = None
    """Descripción del curso (opcional)"""
    maestro: str | None = None
    """Maestro del curso (opcional)"""

    @field_validator("nombre", "descripcion", "maestro")
    @classmethod
    def validate_not_empty(cls, v):
        """Valida que los campos de texto no estén vacíos si se proporcionan."""
        if v is not None and (not v or v.strip() == ""):
            raise ValueError("Campo requerido")
        return v

    class Config:
        """Configuración adicional para el modelo CourseUpdate."""

        json_schema_extra = {
            "examples": [
                {
                    "nombre": "Python avanzado",
                    "descripcion": "Curso avanzado de programación en Python.",
                },
                {
                    "maestro": "Mario Chong",
                },
            ],
        }


class CourseResponse(CursoBase):
    """Esquema para la respuesta de operaciones con cursos."""

    id: int
    """Identificador único del curso en la base de datos"""
    created_at: datetime
    """Fecha y hora de registro del curso en formato ISO 8601"""

    class Config:
        """Configuración adicional para el modelo CourseResponse."""

        orm_mode = True
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "nombre": "Introducción a Python",
                    "descripcion": "Curso básico de programación en Python.",
                    "maestro": "Noe Nieto",
                    "created_at": "2025-02-15T05:00:00",
                },
                {
                    "id": 1,
                    "nombre": "Introducción a Inteligencia Artificial",
                    "descripcion": "Curso básico de Inteligencia Artificial.",
                    "maestro": "Jaime Olvera",
                    "created_at": "2025-05-01T09:00:00",
                },
            ],
        }