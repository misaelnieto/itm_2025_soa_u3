"""All the database models here."""

from sqlmodel import Field, SQLModel


class Agenda(SQLModel, table=True):
    """Modelo para registrar contactos en la base de datos.

    Esta clase representa un contacto en la agenda, con atributos como nombre, teléfono y correo electrónico.
    Se utiliza para interactuar con la tabla `contactos_agenda` en la base de datos.

    Atributos:
        - **id (int | None)**: Identificador único del contacto. Es la clave primaria de la tabla.
        - **nombre (str)**: Nombre del contacto. Este campo es obligatorio.
        - **telefono (str)**: Número de teléfono del contacto. Este campo es obligatorio.
        - **correo (str | None)**: Dirección de correo electrónico del contacto. Este campo es opcional.

    Configuración adicional:
        - La tabla asociada a este modelo se llama `contactos_agenda`.
        - Ejemplos de datos JSON para este modelo:
            [
                {"id": 1, "nombre": "Juan Perez", "telefono": "+1234567890", "correo": "juan@example.com"},
                {"id": 2, "nombre": "Maria Lopez", "telefono": "+9876543210", "correo": "maria@example.com"}
            ]
    """

    __tablename__ = "contactos_agenda"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(title="Nombre", nullable=False)
    telefono: str = Field(title="Telefono", nullable=False)
    correo: str | None = Field(title="Correo", nullable=True)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"id": 1 , "nombre": "Juan Perez", "telefono": "+1234567890", "correo": "juan@example.com"},
                {"id": 2, "nombre": "Maria Lopez", "telefono": "+9876543210", "correo": "maria@example.com"},
            ],
        },
    }
    