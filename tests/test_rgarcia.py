"""# 🧪 Test Suite for Recetas API.

This module contains tests for the Recetas API endpoints. It verifies the following:
- Acces to the list of recipes
- Access to an existing recipe
- Error when trying to access a non-existent recipe
- Update an existing recipe
- Error when trying to update a non-existent recipe
- Delete an existing recipe
- Error when trying to delete a non-existent recipe
- Test the now_utc function
"""

from datetime import UTC, datetime

from fastapi import status
from fastapi.testclient import TestClient

from app.proyectos.rgarcia.models import Receta, now_utc

BASE_PATH = "/api/v1/rgarcia/recetas"

    
def test_all_recipes(rest_api: TestClient):
    """Test the method to get the list of Recipes from the API."""
    response = rest_api.get(f"{BASE_PATH}/todas")
    assert response.status_code == status.HTTP_200_OK

    # Expected a list of Receta objects
    assert isinstance(response.json(), list) 

    # All items in the list are Receta objects
    assert all(isinstance(item, Receta) for item in response.json()) 


def test_existent_singular_recipe(rest_api: TestClient):
    """Test the method to get a single Recipe by its ID."""
    # Create a new Recipe with ID 1
    receta_id = 1
    receta_data = {
        "id": receta_id,
        "nombre": "Test Recipe",
        "descripcion": "Test",
        "min_preparacion": 50,
        "metodo_preparacion": "Test de metodo",
        "ingredientes": "Test Ingredients",
        "created_at": "2022-01-01T00:00:00",
        }

    # Call the API to create the recipe
    create_response = rest_api.post(f"{BASE_PATH}/alta", json=receta_data)
    assert create_response.status_code == status.HTTP_200_OK
    
    # Call the API to get the recipe by its ID
    response = rest_api.get(f"{BASE_PATH}/receta", params={"receta_id": receta_id})
    
    # Check that the response is OK
    assert response.status_code == status.HTTP_200_OK
    
    receta_data = response.json()
    # Expect a Dictionary
    assert isinstance(receta_data, dict) is True
    # Parse the response into a Receta object
    receta = Receta.model_validate(receta_data)
    # Check that the parsed data is an instance of Receta
    assert isinstance(receta, Receta)


def test_non_existent_recipe(rest_api: TestClient):
    """Test the method to get a single Recipe by its ID when it does not exist."""
    response = rest_api.get(f"{BASE_PATH}/receta", params={"receta_id": 2})
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_existent_recipe(rest_api: TestClient):
    """Test the method to update a Recipe by its ID."""
    # Create a new Recipe with ID 1
    receta_id = 1
    receta_data = {
        "id": receta_id,
        "nombre": "Test Recipe",
        "descripcion": "Test",
        "min_preparacion": 50,
        "metodo_preparacion": "Test de metodo",
        "ingredientes": "Test Ingredients",
        "created_at": "2022-01-01T00:00:00",
        }

    # Call the API to create the recipe
    create_response = rest_api.post(f"{BASE_PATH}/alta", json=receta_data)
    assert create_response.status_code == status.HTTP_200_OK
    
    receta_data = {
        "id": receta_id,
        "nombre": "Test Recipe Updated",
        "descripcion": "Test",
        "min_preparacion": 50,
        "metodo_preparacion": "Test de metodo",
        "ingredientes": "Test Ingredients",
        "created_at": "2022-01-01T00:00:00",
        }
    # Call the API to modify the recipe by its ID
    response = rest_api.put(f"{BASE_PATH}/modificar", json=receta_data)
    
    # Check that the response is OK
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Call the API to get the modified recipe by its ID
    response = rest_api.get(f"{BASE_PATH}/receta", params={"receta_id": receta_id})
    
    # Check that the response is OK
    assert response.status_code == status.HTTP_200_OK

    # Parse the response into a Receta object
    receta = Receta.model_validate(response.json())
    # Check that the parse
    assert receta.nombre == "Test Recipe Updated"

def test_update_non_existent_recipe(rest_api: TestClient):
    """Test the method to update a Recipe that doesn't exist."""
    receta_id = 1
    receta_data = {
        "id": receta_id,
        "nombre": "Test Recipe Updated",
        "descripcion": "Test",
        "min_preparacion": 50,
        "metodo_preparacion": "Test de metodo",
        "ingredientes": "Test Ingredients",
        "created_at": "2022-01-01T00:00:00",
        }
    # Call the API to modify the recipe by its ID
    response = rest_api.put(f"{BASE_PATH}/modificar", json=receta_data)
    
    # Check that the response is NOT FOUND
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_existent_recipe(rest_api: TestClient):
    """Test the method to update a Recipe by its ID."""
    # Create a new Recipe with ID 1
    receta_id = 1
    receta_data = {
        "id": receta_id,
        "nombre": "Test Recipe",
        "descripcion": "Test",
        "min_preparacion": 50,
        "metodo_preparacion": "Test de metodo",
        "ingredientes": "Test Ingredients",
        "created_at": "2022-01-01T00:00:00",
        }

    # Call the API to create the recipe
    create_response = rest_api.post(f"{BASE_PATH}/alta", json=receta_data)
    assert create_response.status_code == status.HTTP_200_OK
    
    response = rest_api.delete(f"{BASE_PATH}/eliminar", params={"receta_id": receta_id})
    
    # Check that the response is OK
    assert response.status_code == status.HTTP_200_OK
    
    # Call the API to try to get the deleted recipe by its ID
    response = rest_api.get(f"{BASE_PATH}/receta", params={"receta_id": receta_id})
    
    # Check that the response is NOT FOUND
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_non_existent_recipe(rest_api: TestClient):
    """Test the method to update a Recipe by its ID."""
    # Create a new Recipe with ID 1
    receta_id = 1
    
    response = rest_api.delete(f"{BASE_PATH}/eliminar", params={"receta_id": receta_id})
    
    # Check that the response is NOT FOUND
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_now_utc():
    """Test the now_utc function."""
    # Call the function
    result = now_utc()

    # Check if the result is a datetime object
    assert isinstance(result, datetime), f"Expected datetime, but got {type(result)}"

    # Check if the result is in UTC (the timezone should be UTC)
    assert result.tzinfo == UTC, f"Expected UTC timezone, but got {result.tzinfo}"

    # Check if the result is close to the current UTC time within a reasonable margin
    now = datetime.now(UTC)  # Get the current UTC time for comparison
    time_difference = abs((now - result).total_seconds())
    assert time_difference < 1, f"Time difference is too large: {time_difference} seconds"

