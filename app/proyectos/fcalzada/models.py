"""Modelos para la base de datos de Registro de Carros."""
from sqlmodel import Field, SQLModel


class Car(SQLModel, table=True):
    """Modelo que representa un carro registrado en la base de datos.

    Atributos:
        id (int | None): Identificador único del carro. Es la clave primaria.
        quantity (int): Cantidad de carros en el registro. Fijado a 1 por defecto.
        marca (str): Marca del carro. No puede ser nulo.
        modelo (str): Modelo del carro. No puede ser nulo.
        año (int): Año de fabricación del carro. No puede ser nulo.
        color (str): Color del carro. No puede ser nulo.

    Configuración:
        __tablename__: Nombre de la tabla en la base de datos (`registro_carro`).
        model_config: Configuración adicional para la visualización del esquema JSON, 
                      incluyendo ejemplos de registros de carros.
    """

    __tablename__ = "registro_carro"
    id: int | None = Field(default=None, primary_key=True)
    """Identificador único del carro. Clave primaria (opcional en la creación)."""
    quantity: int = Field(title="Cantidad", default=1, nullable=False)  # 'quantity' fijo a 1
    """Cantidad de carros en el registro. Fijado a 1 por defecto."""
    marca: str = Field(title="Marca", nullable=False)  # Atributo de marca
    """Marca del carro. No puede ser nulo."""
    modelo: str = Field(title="Modelo", nullable=False)  # Atributo de modelo
    """Modelo del carro. No puede ser nulo."""
    año: int = Field(title="Año", nullable=False)  # Atributo de año
    """Año de fabricación del carro. No puede ser nulo."""
    color: str = Field(title="Color", nullable=False)  # Atributo de color
    """Color del carro. No puede ser nulo."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "quantity": 1,  # Ejemplo de registro de un carro
                    "id": 1,
                    "marca": "Honda",
                    "modelo": "Crv",
                    "año": 2007,
                    "color": "Gris",
                },
                {
                    "quantity": 1,  # Ejemplo de registro de un carro
                    "id": 5,
                    "marca": "Honda",
                    "modelo": "Civic",
                    "año": 2021,
                    "color": "Negro",
                },
            ],
        },
    }
