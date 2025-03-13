import importlib
import logging
import pkgutil
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic_settings import BaseSettings
from sqlmodel import Session, SQLModel, create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("fastapi")
logger.setLevel(logging.DEBUG)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    verbose: bool = True
    database_url: str = "sqlite:///./database.db"
    site_title: str = "Unidad 3 - Aplicaciones web con REST"
    site_description: str = (
        "Esta aplicación reune todos los proyectos de los estudiantes de la unidad 3"
    )
    site_version: str = "0.1"


settings = Settings()
engine = create_engine(settings.database_url, connect_args = {"check_same_thread": False})


@lru_cache()
def get_settings() -> Settings:
    """Configure the program settings."""
    return Settings()


def create_db_and_tables():
    """This is a callback function that creates the database and tables on startup."""
    package = importlib.import_module("app.proyectos")
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if not is_pkg:
            continue
        spec = importlib.util.find_spec(f"app.proyectos.{module_name}.models")
        if spec is None:
            logger.warning(
                f"El módulo {module_name} no tiene un archivo models.py. Ignorando..."
            )
            continue
        models_module = spec.loader.load_module()
        for obj in [getattr(models_module, a) for a in dir(models_module) if not a.startswith("__")]:
            if isinstance(obj, type) and issubclass(obj, SQLModel) and hasattr(obj, "__table__"):
                # Import the module to populate the metadata from SQLModel
                # See https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/?h=metadat#sqlmodel-metadata-order-matters
                importlib.import_module(f"app.proyectos.{module_name}.models")
    
    engine = create_engine(settings.database_url)
    SQLModel.metadata.create_all(
        engine,
    )


def get_session():
    """
    Esta función crea una sesión (conexión) a la base de datos y la cierra al finalizar.
    """
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_session)]

def recolecta_rutas(app: FastAPI):
    package = importlib.import_module("app.proyectos")

    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if not is_pkg:
            continue
        spec = importlib.util.find_spec(f"app.proyectos.{module_name}.routes")
        if spec is None:
            logger.warning(
                f"El módulo {module_name} no tiene un archivo routes.py. Ignorando..."
            )
            continue
        route_module = spec.loader.load_module()
        if hasattr(route_module, "router"):
            app_path = f"/api/v1/{module_name}"
            logger.info(f"Instalando app  en {app_path}")
            app.include_router(route_module.router, prefix=app_path)


async def lifespan_cycle(app: FastAPI):
    create_db_and_tables()
    recolecta_rutas(app)
    yield

app = FastAPI(
    title=settings.site_title,
    description=settings.site_description,
    version=settings.site_version,
    lifespan=lifespan_cycle,
)
