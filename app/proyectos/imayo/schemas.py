"""Esquemas para los eventos.

Este módulo define los esquemas utilizados para la creación, lectura y validación de eventos.

Esquemas:
    - `EventBase`: Esquema base para los eventos.
    - `EventCreate`: Esquema para crear un evento.
    - `EventRead`: Esquema para leer los detalles de un evento.

Funciones:
    - No hay funciones definidas en este módulo, solo esquemas para representar los datos de los eventos.

Dependencias:
    - [Pydantic](https://pydantic-docs.helpmanual.io/): Biblioteca para la validación y gestión de datos en Python.
    - [datetime](https://docs.python.org/3/library/datetime.html): Módulo de Python para manejar fechas y horas.
"""

from datetime import datetime

from pydantic import BaseModel


class EventBase(BaseModel):
    """Esquema base para un evento.

    Este esquema contiene los campos comunes a la creación y lectura de eventos.

    - **nombre** (tipo: `str`): El nombre del evento.
    - **descripcion** (tipo: `str | None`): Una descripción opcional del evento.
    - **fecha** (tipo: `datetime`): La fecha y hora del evento.
    """

    nombre: str
    descripcion: str | None = None
    fecha: datetime

class EventCreate(EventBase):
    """Esquema para crear un evento.

    Este esquema hereda de `EventBase` y se utiliza para la creación de un nuevo evento.
    No contiene campos adicionales respecto al esquema base.
    """
class EventRead(EventBase):
    """Esquema para leer un evento.

    Este esquema hereda de `EventBase` y se utiliza para la representación de un evento en la base de datos.

    - **id** (tipo: `int`): El identificador único del evento en la base de datos.
    - **created_at** (tipo: `datetime`): La fecha y hora de creación del evento.
    """

    id: int
    created_at: datetime

    class Config:
        """Configuración del modelo.

        Se utiliza para permitir que Pydantic reciba atributos directamente de los objetos ORM,
        como los modelos de SQLModel.
        """

        from_attributes = True


