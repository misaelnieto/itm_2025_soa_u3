"""Esquemas para la API de eventos.

Este módulo define el modelo `Event` para registrar los eventos en la base de datos utilizando SQLModel.

Funciones:
    - `now_utc`: Obtiene la fecha y hora actual en UTC.

Modelos:
    - `Event`: Modelo que representa un evento en la base de datos, con campos como nombre, descripción, fecha y la fecha de creación.

Dependencias:
    - [SQLModel](https://sqlmodel.tiangolo.com/): ORM utilizado para interactuar con la base de datos.
    - [datetime](https://docs.python.org/3/library/datetime.html): Módulo de Python para trabajar con fechas y horas.
"""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def now_utc():
    """Obtener la fecha y hora actual en UTC.

    Esta función devuelve la fecha y hora actuales en formato UTC.

    **Retorno**:
        - `datetime`: La fecha y hora actual en UTC.
    """
    return datetime.now(UTC)


class Event(SQLModel, table=True):
    """Modelo para registrar eventos en la base de datos.

    Este modelo define los atributos necesarios para almacenar información sobre los eventos.

    Atributos:
        - `id` (int | None): Identificador único del evento. Es la clave primaria.
        - `nombre` (str): Nombre del evento. No puede ser nulo.
        - `descripcion` (Optional[str]): Descripción del evento. Puede ser nulo.
        - `fecha` (datetime): Fecha y hora del evento. No puede ser nulo.
        - `created_at` (datetime): Fecha y hora de creación del registro. No puede ser nulo.

    Ejemplos de uso:
        - **Evento 1**:
            - Nombre: Conferencia de Tecnología
            - Descripción: Un evento sobre las últimas tendencias en tecnología.
            - Fecha: 2025-06-15T10:00:00
            - Creado en: 2025-03-25T00:00:00
        - **Evento 2**:
            - Nombre: Taller de Programación en Python
            - Descripción: Aprende a desarrollar aplicaciones con Python.
            - Fecha: 2025-07-10T14:00:00
            - Creado en: 2025-03-25T00:00:00
    """

    __tablename__ = "eventos_event"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(title="Nombre", nullable=False)
    descripcion: str | None = Field(title="Descripción", nullable=True)
    fecha: datetime = Field(title="Fecha del Evento", nullable=False)
    created_at: datetime = Field(
        title="Created At",
        default_factory=now_utc,
        nullable=False,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "nombre": "Conferencia de Tecnología",
                    "descripcion": "Un evento sobre las últimas tendencias en tecnología.",
                    "fecha": "2025-06-15T10:00:00",
                    "created_at": "2025-03-25T00:00:00",
                },
                {
                    "id": 2,
                    "nombre": "Taller de Programación en Python",
                    "descripcion": "Aprende a desarrollar aplicaciones con Python.",
                    "fecha": "2025-07-10T14:00:00",
                    "created_at": "2025-03-25T00:00:00",
                },
            ],
        },
    }


