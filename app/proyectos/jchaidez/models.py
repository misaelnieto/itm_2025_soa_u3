"""Modelo de la base de datos para la API de Gestión de Cursos."""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def now_utc():
    """Se obtiene la fecha y hora actual en UTC.
    
    Está función es utilizada como un valor predeterminado para el campo creted_at en los modelos de la base de datos.
    
    Returns:
        datetime: Fecha y hora actual en formato UTC.
    
    """
    return datetime.now(UTC)

class Register(SQLModel, table=True):
    """Modelo para registrar cursos en la base de datos."""
    
    __tablename__ = "cursos" #Nombre de la tabla en la base de datos.
    id: int | None = Field(default=None, primary_key=True) #Id único del curso.
    nombre: str = Field(title="Nombre", nullable=False) #Nombre del curso.
    descripcion: str = Field(title="Descripción", nullable=True) #Descripción del curso.
    maestro: str = Field(title="Maestro", nullable=False) #Maestro que imparte el curso.
    created_at: datetime = Field(
        title="Created At",
        default_factory=now_utc,
        nullable=False,
    ) #Fecha y hora de registro del curso.

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "nombre": "Introducción a Python",
                    "descripcion": "Curso básico de programación en Python.",
                    "maestro": "Noe Nieto",
                    "created_at": "2025-02-15T05:00:00",
                },
                {
                    "id": 2,
                    "nombre": "Introducción a Inteligencia Artificial",
                    "descripcion": "Curso básico de Inteligencia Artificial.",
                    "maestro": "Jaime Olvera",
                    "created_at": "2025-05-01T09:00:00",
                },
            ],
        },
    }
