"""# 🧪 Test Suite for Alcancia API.

This module contains tests for the Alcancia API endpoints. It verifies the following:
- ✅ The behavior of the API when the database is empty.
- 💰 Deposit transactions.
- 💸 Withdrawal transactions.
- 🔍 Validation of input data for transactions.
"""

from fastapi import status
from fastapi.testclient import TestClient

from app.proyectos.imoreno.models import Operation
from app.proyectos.imoreno.schemas import OperationResponse, OperationResult, OperationType

BASE_PATH = "/api/v1/imoreno/hotel"

def test_empty_database(rest_api: TestClient):
    """🗃️ Tests the API with an empty database."""
    response = rest_api.get(f"{BASE_PATH}/operations")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_operation_add(rest_api: TestClient):
    """Test adding and updating operations."""
    # First to test an incorrect operation type
    response = rest_api.post(
        f"{BASE_PATH}/operations/{OperationType.delete}/",
        json={"first_name": "Isaí", "middle_name": "Moreno", "last_name": "Mendoza", "email": "isaimmoreno@gmail.com", "check_in": "2025-03-13T07:48:04.965275", "room": 1},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Then operations db is empty and we're gonna add a client to db
    response = rest_api.post(
        f"{BASE_PATH}/operations/{OperationType.add}/",
        json={"first_name": "Isaí", "middle_name": "Moreno", "last_name": "Mendoza", "email": "isaimmoreno@gmail.com", "check_in": "2025-03-13T07:48:04.965275", "room": 1},
    )
    assert response.status_code == status.HTTP_201_CREATED
    r = OperationResponse(**response.json())
    assert r.result == OperationResult.success
    # Now we have one client in the database
    response = rest_api.get(f"{BASE_PATH}/operations")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    

def test_operation_update(rest_api: TestClient):
    """Test by adding and updating operations."""
    #First it's going to test if the operation type is incorrect
    response = rest_api.put(
        f"{BASE_PATH}/operations/{OperationType.list}/",
        json={"first_name": "Jordan", "middle_name": "Ochoa", "last_name": "Rios", "email": "jordan@ooutlook.com", "check_in": "2025-03-13T07:48:04.965275", "room": 5},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # The operations db is empty and we're gonna add a client to db
    response = rest_api.post(
        f"{BASE_PATH}/operations/{OperationType.add}/",
        json={"first_name": "Jordan", "middle_name": "Ochoa", "last_name": "Rios", "email": "jordan@ooutlook.com", "check_in": "2025-03-13T07:48:04.965275", "room": 5},
    )

    # Now we are going to update the client's room
    response = rest_api.put(
        f"{BASE_PATH}/operations/{OperationType.update}",
        json={"first_name": "Jordan", "middle_name": "Ochoa", "last_name": "Rios", "room": 2},
    )
    assert response.status_code == status.HTTP_200_OK
    r = OperationResponse(**response.json())
    # Now we are going to check that the room has changed
    assert r.previous_data != r.data
    # Now we have two clients in the database
    response = rest_api.get(f"{BASE_PATH}/operations")
    assert response.status_code == status.HTTP_200_OK
    # We are going to try to update the room of a client that does not exist
    response = rest_api.put(
        f"{BASE_PATH}/operations/{OperationType.update}/",
        json={"first_name": "Diana", "middle_name": "Laura", "last_name": "Mendoza", "room": 2},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_operation_search(rest_api: TestClient):
    """Test by adding and searching operations."""
    #First it's going to test if the operation type is incorrect
    response = rest_api.get(
        f"{BASE_PATH}/operations/{OperationType.delete}/",
        params={"first_name": "Jordan", "middle_name": "Ochoa", "last_name": "Rios", "email": "jordan@ooutlook.com", "check_in": "2025-03-13T07:48:04.965275", "room": 5},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Then we add a new client
    response = rest_api.post(
        f"{BASE_PATH}/operations/{OperationType.add}/",
        json={
            "first_name": "Raul",
            "middle_name": "Rentería",
            "last_name": "Gastelum",
            "email": "raul@protonmail.com",
            "check_in": "2025-03-13T07:48:04.965275",
            "room": 19,
        },
    )
    # Now we are going to search for the client
    response = rest_api.get(
        f"{BASE_PATH}/operations/{OperationType.search}",
        params={
            "first_name": "Raul",
            "middle_name": "Rentería",
            "last_name": "Gastelum",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    
def test_operation_delete(rest_api: TestClient):
    """Test the delete operation by searching and deleting a client."""
    # First it checks if endpoint returns 400 if the operation type is incorrect
    response = rest_api.delete(
        f"{BASE_PATH}/operations/{OperationType.list}",
        params={
            "first_name": "Juan",
            "middle_name": "García",
            "last_name": "Lopez",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Now we add a new client
    response = rest_api.post(
        f"{BASE_PATH}/operations/{OperationType.add}/",
        json={
            "first_name": "Juan",
            "middle_name": "García",
            "last_name": "Lopez",
            "email": "juan@gmail.com",
            "check_in": "2025-03-13T07:48:04.965275",
            "room": 20,
        },
    )
    # It's gonna test deleting a client that does not exist
    response = rest_api.delete(
        f"{BASE_PATH}/operations/{OperationType.delete}",
        params={
            "first_name": "Luisa",
            "middle_name": "Reyes",
            "last_name": "Moreno",
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Now we are going to delete the client
    response = rest_api.delete(
        f"{BASE_PATH}/operations/{OperationType.delete}",
        params={
            "first_name": "Juan",
            "middle_name": "García",
            "last_name": "Lopez",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    r = OperationResponse(**response.json())
    assert r.result == OperationResult.success

def test_operation_list(rest_api: TestClient):
    """Test the list operation."""
    response = rest_api.get(f"{BASE_PATH}/operations/{OperationType.list}")
    assert response.status_code == status.HTTP_200_OK

def test_operation_model():
    """Prueba la creación directa de un modelo Operation."""
    # Crear una instancia del modelo
    operation = Operation(
        first_name="Esperanza",
        middle_name="Guillén",
        last_name="Sánchez",
        email="esperanza@yahoo.com",
        room=101,
    )
    
    # Verificar que la instancia se creó correctamente
    assert operation.first_name == "Esperanza"
    assert operation.middle_name == "Guillén"
    assert operation.last_name == "Sánchez"
    assert operation.email == "esperanza@yahoo.com"
    assert operation.room == 101
    assert operation.check_in is not None  # Verifica que se estableció la fecha por defecto
    assert operation.client_id is None  # El ID debe ser None hasta que se guarde en la BD