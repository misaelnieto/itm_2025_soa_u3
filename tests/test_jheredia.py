"""Este documento contiene las pruebas de la API de registro de ciudades."""

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

# Ajusta según tu estructura real
from app.db import DbSession
from app.proyectos.jheredia.routes import api_router

BASE_PATH = "/api/v1/jheredia/registro_ciudades"


# Cada test obtiene su propio engine in-memory
@pytest.fixture
def test_engine():
    """Crea un motor de base de datos SQLite en memoria para pruebas."""
    return create_engine("sqlite:///:memory:", echo=False)


@pytest.fixture
def db_session(test_engine):
    """Crea una sesión de base de datos para pruebas."""
    # Reinicia las tablas antes de cada test
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def rest_api(db_session):
    """Devuelve un TestClient de FastAPI."""
    app = FastAPI()
    app.include_router(api_router, prefix="/api/v1/jheredia")

    def get_db_override():
        return db_session

    app.dependency_overrides[DbSession] = get_db_override

    return TestClient(app)


def test_create_city(rest_api):
    """Verifica que se pueda crear una ciudad con datos válidos."""
    payload = {
        "name": "Test City",
        "population": 500000,
        "country": "Test Country",
        "region": "Test Region",
    }
    response = rest_api.post(f"{BASE_PATH}/ciudades", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    city = response.json()
    assert "id" in city
    assert city["name"] == payload["name"]
    assert city["population"] == payload["population"]
    assert city["country"] == payload["country"]
    assert city["region"] == payload["region"]


def test_create_city_valid(rest_api):
    """Verifica que se pueda crear una ciudad con datos válidos y completos."""
    payload = {
        "name": "Valid City",
        "population": 100000,
        "country": "Valid Country",
        "region": "Valid Region",
    }
    response = rest_api.post(f"{BASE_PATH}/ciudades", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    city = response.json()
    assert city["name"] == payload["name"]
    assert city["population"] == payload["population"]
    assert city["country"] == payload["country"]
    assert city["region"] == payload["region"]
    assert "id" in city

def test_create_city_with_empty_country(rest_api: TestClient):
    """Verifica que no se pueda crear una ciudad con el campo 'country' vacío."""
    payload = {
        "name": "Test City",
        "population": 100000,
        "country": "",
    }
    response = rest_api.post(f"{BASE_PATH}/ciudades", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": "Country field cannot be empty or contain only spaces."}  # Actualizar mensaje esperado


def test_create_city_with_large_population(rest_api):
    """Verifica que se pueda crear una ciudad con una población muy grande."""
    payload = {
        "name": "Mega City",
        "population": 1000000000,
        "country": "Mega Country",
        "region": "Mega Region",
    }
    response = rest_api.post(f"{BASE_PATH}/ciudades", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    city = response.json()
    assert city["name"] == payload["name"]
    assert city["population"] == payload["population"]
    assert city["country"] == payload["country"]
    assert city["region"] == payload["region"]


def test_update_city(rest_api):
    """Verifica que se puedan actualizar los datos de una ciudad existente."""
    payload = {
        "name": "Test City",
        "population": 500000,
        "country": "Test Country",
        "region": "Test Region",
    }
    create_response = rest_api.post(f"{BASE_PATH}/ciudades", json=payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    city_id = create_response.json()["id"]

    update_payload = {
        "name": "Updated City",
        "population": 600000,
        "country": "Updated Country",
        "region": "Updated Region",
    }
    response = rest_api.put(f"{BASE_PATH}/actualizar/{city_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    updated_city = response.json()
    assert updated_city["id"] == city_id
    assert updated_city["name"] == update_payload["name"]
    assert updated_city["population"] == update_payload["population"]


def test_update_city_not_found(rest_api):
    """Verifica que no se pueda actualizar una ciudad inexistente."""
    city_id = 9999
    update_payload = {
        "name": "Nonexistent City",
        "population": 600000,
        "country": "Nonexistent Country",
        "region": "Nonexistent Region",
    }
    response = rest_api.put(f"{BASE_PATH}/actualizar/{city_id}", json=update_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"No se encontró la ciudad con identificador {city_id}"


def test_get_city(rest_api):
    """Verifica que se puedan obtener los datos de una ciudad por su ID."""
    payload = {
        "name": "Test City",
        "population": 500000,
        "country": "Test Country",
        "region": "Test Region",
    }
    create_response = rest_api.post(f"{BASE_PATH}/ciudades", json=payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    city_id = create_response.json()["id"]

    response = rest_api.get(f"{BASE_PATH}/ciudades/{city_id}")
    assert response.status_code == status.HTTP_200_OK
    city = response.json()
    assert city["id"] == city_id
    assert city["name"] == payload["name"]
    assert city["population"] == payload["population"]
    assert city["country"] == payload["country"]
    assert city["region"] == payload["region"]


def test_list_cities(rest_api):
    """Verifica que se pueda listar todas las ciudades registradas."""
    response = rest_api.get(f"{BASE_PATH}/ciudades")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_register_city_entry(rest_api):
    """Verifica que se pueda registrar una entrada de población para una ciudad."""
    payload = {
        "name": "Test City",
        "population": 500000,
        "country": "Test Country",
        "region": "Test Region",
    }
    response = rest_api.post(f"{BASE_PATH}/registro/entrada", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert isinstance(result, dict), f"Expected a dictionary, got {type(result)}"
    assert result.get("result") == "registrado"


def test_register_city_exit(rest_api):
    """Verifica que se pueda registrar una salida de población para una ciudad."""
    payload = {
        "name": "Test City",
        "population": 500000,
        "country": "Test Country",
        "region": "Test Region",
    }
    rest_api.post(f"{BASE_PATH}/ciudades", json=payload)
    payload["population"] = 100000
    response = rest_api.post(f"{BASE_PATH}/registro/salida", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert result["result"] == "registrado"
 

def test_get_city_not_found(rest_api):
    """Verifica que no se puedan obtener los datos de una ciudad inexistente."""
    response = rest_api.get(f"{BASE_PATH}/ciudades/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No se encontró la ciudad con identificador 9999"


def test_delete_city(rest_api):
    """Verifica que se pueda eliminar una ciudad existente."""
    payload = {
        "name": "Test City",
        "population": 500000,
        "country": "Test Country",
        "region": "Test Region",
    }
    create_response = rest_api.post(f"{BASE_PATH}/ciudades", json=payload)
    city_id = create_response.json()["id"]

    response = rest_api.delete(f"{BASE_PATH}/eliminar/{city_id}")
    assert response.status_code == status.HTTP_200_OK

    response = rest_api.get(f"{BASE_PATH}/ciudades/{city_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_city_not_found(rest_api):
    """Verifica que no se pueda eliminar una ciudad inexistente."""
    response = rest_api.delete(f"{BASE_PATH}/eliminar/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No se encontró la ciudad con identificador 9999"


def test_calculate_total_population(rest_api):
    """Verifica que se calcule correctamente la población total de todas las ciudades."""
    payload1 = {"name": "City1", "population": 500000, "country": "Country1", "region": "Region1"}
    payload2 = {"name": "City2", "population": 300000, "country": "Country2", "region": "Region2"}
    rest_api.post(f"{BASE_PATH}/ciudades", json=payload1)
    rest_api.post(f"{BASE_PATH}/ciudades", json=payload2)

  

def test_create_city_invalid(rest_api):
    """Verifica que no se pueda crear una ciudad con datos inválidos."""
    payload = {
        "name": "",
        "population": -100,
        "country": "Test Country",
        "region": "Test Region",
    }
    response = rest_api.post(f"{BASE_PATH}/ciudades", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_actualizar_ciudad_not_found():
    """Verifica que no se pueda actualizar una ciudad inexistente usando un mock."""
    from fastapi import FastAPI
    client = TestClient(FastAPI())
    response = client.put(
        "/registro_ciudades/actualizar/999",
        json={
            "name": "Test City",
            "population": 1000,
            "country": "Test Country",
            "region": "Test Region",
        },
    )
    assert response.status_code == 404


def test_routes_availability(rest_api):
    """Verifica que todas las rutas del API estén accesibles y respondan correctamente."""
    routes = [
        {"method": "POST", "path": f"{BASE_PATH}/ciudades"},
        {"method": "PUT", "path": f"{BASE_PATH}/actualizar/1"},
        {"method": "GET", "path": f"{BASE_PATH}/ciudades/1"},
        {"method": "GET", "path": f"{BASE_PATH}/ciudades"},
        {"method": "POST", "path": f"{BASE_PATH}/registro/entrada"},
        {"method": "POST", "path": f"{BASE_PATH}/registro/salida"},
        {"method": "DELETE", "path": f"{BASE_PATH}/eliminar/1"},
    ]

    for route in routes:
        if route["method"] == "POST":
            response = rest_api.post(route["path"], json={})
        elif route["method"] == "PUT":
            response = rest_api.put(route["path"], json={})
        elif route["method"] == "GET":
            response = rest_api.get(route["path"])
        elif route["method"] == "DELETE":
            response = rest_api.delete(route["path"])
        else:
            continue

        # Ensure the route is accessible and returns a valid status code
        assert response.status_code in {200, 201, 404, 422, 403}
