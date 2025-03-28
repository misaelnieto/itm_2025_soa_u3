"""All the database models here."""

from sqlmodel import Field, SQLModel

# default_factory es para contenido dinamico, y normalmente utiliza una funcion
# default es para contenido estatico


class Peliculas(SQLModel, table=True):
    """Modelo para crear tabla peliculas."""

    __tablename__ = "tabla peliculas"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(title="nombre", nullable=False)
    director: str = Field(title="director", nullable=False)
    release: str = Field(title="fecha de lanzamiento", nullable=False)


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 18,
                    "name": "Titanic",
                    "director":"James Cameron",
                    "release": "1995-12-19T00:00:00.000000",
                },
                {
                    "id": 34,
                    "name": "Spiderman",
                    "director":"Sam Raim",
                    "release": "2002-05-03T00:00:00.000000",
                },
            ],
        },
    }
