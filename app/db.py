"""Database-related functionalities for our REST server.

It includes the following components:
- `engine`: The SQLAlchemy engine created using the database URL from the settings.
- `initialize_database`: An asynchronous function to create the database and tables by importing models from the `app.proyectos` package.
- `get_session`: An asynchronous generator function to provide a database session.
- `DbSession`: A dependency that provides a database session using FastAPI's `Depends`.

Functions:
- `initialize_database()`: Imports models from the `app.proyectos` package and creates the database tables.
- `get_session()`: Provides a database session for dependency injection in FastAPI routes.

Dependencies:
- `DbSession`: Annotated dependency for injecting a database session into FastAPI routes.
"""

import importlib
import pkgutil
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from app.config import settings
from app.log_utils import logger

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})


def initialize_database(db_engine: Engine = engine):
    """Import SQLModel models from the `app.proyectos` package to create database tables."""
    package = importlib.import_module("app.proyectos")
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if not is_pkg:
            continue
        models_module = f"app.proyectos.{module_name}.models"
        spec = importlib.util.find_spec(f"app.proyectos.{module_name}.models")
        if spec is None or spec.loader is None:
            logger.warning(
                f"El módulo {module_name} no tiene un archivo models.py. Ignorando...",
            )
            continue
        # Import the module to populate the metadata from SQLModel
        # See https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/?h=metadat#sqlmodel-metadata-order-matters
        importlib.import_module(models_module)
    SQLModel.metadata.create_all(
        db_engine,
    )


def drop_database(db_engine: Engine = engine):
    """Drop all the tables that were created using SQLModel.

    If you are unsure whether you need this, then don't use it.
    Only use this for testing, or if you _really_ know what you are doing, or else you're gonna have a bad time!
    """
    logger.warning("Cleaning database")
    SQLModel.metadata.drop_all(db_engine)


def get_session():
    """Provide a database session for dependency injection in FastAPI routes."""
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_session)]
