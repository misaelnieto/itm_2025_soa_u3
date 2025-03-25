"""All the database models here."""

from sqlmodel import Field, SQLModel


class Agenda(SQLModel, table=True):
    """Modelo para registrar contactos en la base de datos."""

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
    