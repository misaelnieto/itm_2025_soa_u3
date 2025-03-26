"""Main module for the FastAPI application.

This module is responsible for setting up and running the FastAPI application.
It includes the following key functionalities:

- Loading and registering routes from all modules in the 'app.proyectos' package.
- Creating the database and tables on startup using lifecycle events.

Functions:
    - `load_routes(app: FastAPI)`: Loads and registers routes from all modules in
      the 'app.proyectos' package. This function is responsible for locating the
      routes you define in your project modules and including them in the main
      application.
    - `lifespan_cycle(app: FastAPI)`: Lifecycle event handler for the FastAPI
      application. This function locates all the database models in your project
      and creates the tables in the database when the server starts up.

Classes:
    - None

Dependencies:
    - `fastapi`: FastAPI framework for building APIs.
    - `importlib`: Standard library module for importing modules.
    - `pkgutil`: Standard library module for working with packages.
    - `app.config`: Module containing application settings.
    - `app.db`: Module containing database setup functions.
    - `app.log_utils`: Module containing logging configuration.

Author:
    - Noe Nieto <noemisael.nieto@itmexicali.edu.mx>

License:
    - MIT License
"""

import importlib
import pkgutil

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import initialize_database
from app.log_utils import logger


def load_routes(app: FastAPI):
    """Load and register routes from all modules in the 'app.proyectos' package.

    This function dynamically imports and registers API and frontend routes
    from all modules in the 'app.proyectos' package. It looks for 'routes.py'
    files in each module and includes the routers defined in them.

    Args:
        app (FastAPI): The FastAPI application instance.

    """
    package = importlib.import_module("app.proyectos")

    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if not is_pkg:
            continue
        routes_module = f"app.proyectos.{module_name}.routes"
        try:
            routes = importlib.import_module(routes_module)
            if hasattr(routes, "api_router"):
                app_path = f"/api/v1/{module_name}"
                logger.info(f"Instalando ruta de API en {app_path}")
                app.include_router(routes.api_router, prefix=app_path)
            if hasattr(routes, "frontend_router"):
                app_path = f"/{module_name}"
                logger.info(f"Instalando ruta de frontend en  {app_path}")
                app.include_router(routes.frontend_router, prefix=app_path)
        except ImportError:
            logger.warning(
                f"El módulo {module_name} no tiene un archivo routes.py o no se puede importar. Ignorando...",
            )


async def lifespan_cycle(app: FastAPI):
    """Lifecycle event handler for the FastAPI application.

    This function is called during the startup and shutdown of the FastAPI
    application. It creates the database and tables, and loads the routes.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None

    For more information on the lifespan parameter, see:
    https://fastapi.tiangolo.com/advanced/events/#lifespan

    """
    logger.info("lifespan_cycle setup")
    initialize_database()
    load_routes(app)
    yield
    logger.info("lifespan_cycle teardown")


app = FastAPI(
    title=settings.site_title,
    summary=settings.site_summary,
    description=settings.site_description,
    version=settings.site_version,
    lifespan=lifespan_cycle,
    contact={
        "name": "Documentación del proyecto",
        "url": "https://misaelnieto.github.io/itm_2005_soa_u3/",
    },
    openapi_tags=[
        {
            "name": "Alcancia",
            "description": "API para el proyecto de **Alcancia**. Sólo contiene 2 rutas.",
        },
    ],
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
