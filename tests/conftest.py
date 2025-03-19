"""Fixtures for setting up and testing the FastAPI application.

Fixtures:
    - `db_engine`: Sets up an in-memory SQLite database for testing.
    - `app`: Configures the FastAPI application with the test database.
    - `rest_api`: Provides a `TestClient` for making HTTP requests to the FastAPI application.

Note:
    The most important fixture in this module is `rest_api`, as it is the one you will use the most
    for testing API endpoints.

"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from app.db import drop_database, get_session, initialize_database
from app.log_utils import logger


@pytest.fixture
def db_engine()-> Engine: # type: ignore
    """Fixture to set up an in-memory SQLite database for testing.

    This fixture creates an empty, in-memory SQLite database, initializes it, and ensures
    proper cleanup after the test.

    Tip: If you are trying to debug database schema issues, temporarily change the database URI to
    `"sqlite:///test.db"`. The database file will be created in the directory where you are running pytest from.

    Yields:
        Engine: The SQLAlchemy engine connected to the in-memory SQLite database.

    """
    logger.info("Database Fixture: setup")
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    initialize_database(engine)
    yield engine
    logger.info("Database Fixture: teardown")
    drop_database(engine)


@pytest.fixture
def app(db_engine):
    """Fixture to set up the FastAPI application for testing.

    This fixture overrides the `get_session` dependency to use the in-memory SQLite database
    and loads the application routes.

    Note:
        Since this fixture depends on `db_engine`, pytest will ensure that the database
        is created and initialized before this fixture is executed.

    Args:
        db_engine (Engine): The SQLAlchemy engine connected to the in-memory SQLite database.

    Yields:
        FastAPI: The FastAPI application instance configured for testing.

    """
    logger.info("App fixture: setup")
    session = Session(db_engine)
    def get_session_override() -> Session:
        return session

    from app.main import app, load_routes
    app.dependency_overrides[get_session] = get_session_override
    load_routes(app)
    yield app
    logger.info("App fixture: teardown")
    session.rollback()
    session.close()


@pytest.fixture
def rest_api(app:FastAPI):
    """Fixture to provide a TestClient for testing the FastAPI application.

    This fixture sets up the FastAPI application and provides a TestClient for making
    HTTP requests to the application. It ensures proper setup and teardown of the client.

    Args:
        app (FastAPI): The FastAPI application instance configured for testing.

    Yields:
        TestClient: A client for testing the FastAPI application.

    Example:
        Here's an example of a test using the `rest_api` fixture:

        ```python
        def test_empty_database(rest_api):
            \"\"\"Tests the API with an empty database.\"\"\"
            response = rest_api.get(f"{BASE_PATH}/transactions")
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == []
        ```

    """
    logger.info("rest_api Fixture: setup")
    client = TestClient(app)
    try:
        yield client
    finally:
        client.close()
        logger.info("rest_api Fixture: teardown")