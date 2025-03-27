"""# 🧪 Test Suite for Animals API.

This module contains tests for the Animals API endpoints. It verifies the following:
- ✅ The behavior of the API when the database is empty.
- 🐾 Create animal records.
- ✏️ Update animal records.
- 🗑️ Delete animal records.
- 🔍 Validation of input data for animal records.
"""

from fastapi import status

from app.proyectos.asantelis.schemas import AnimalResponse

BASE_PATH = "/api/v1/asantelis/animales"


def test_empty_database(rest_api):
    """🗃️ Tests the API with an empty database."""
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_animal(rest_api):
    """🐾 Test creating animal records."""
    # First, the database is empty
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    # Now let's create a new animal
    new_animal = {"nombre": "Firulais", "raza": "Pastor Alemán", "edad": 5}
    response = rest_api.post(f"{BASE_PATH}/", json=new_animal)
    assert response.status_code == status.HTTP_201_CREATED
    r = AnimalResponse(**response.json())
    assert r.nombre == new_animal["nombre"]
    assert r.raza == new_animal["raza"]
    assert r.edad == new_animal["edad"]

    # Verify the animal is in the database
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    animals = response.json()
    assert len(animals) == 1
    assert animals[0]["nombre"] == new_animal["nombre"]
    assert animals[0]["raza"] == new_animal["raza"]
    assert animals[0]["edad"] == new_animal["edad"]


def test_update_animal(rest_api):
    """✏️ Test updating animal records."""
    # First, create a new animal
    new_animal = {"nombre": "Firulais", "raza": "Pastor Alemán", "edad": 5}
    response = rest_api.post(f"{BASE_PATH}/", json=new_animal)
    assert response.status_code == status.HTTP_201_CREATED
    animal_id = response.json()["id"]

    # Update the animal's details
    updated_animal = {"nombre": "Max", "raza": "Labrador", "edad": 6}
    response = rest_api.put(f"{BASE_PATH}/{animal_id}", json=updated_animal)
    assert response.status_code == status.HTTP_200_OK
    r = AnimalResponse(**response.json())
    assert r.nombre == updated_animal["nombre"]
    assert r.raza == updated_animal["raza"]
    assert r.edad == updated_animal["edad"]

    # Verify the animal's details have been updated in the database
    response = rest_api.get(f"{BASE_PATH}/{animal_id}")
    assert response.status_code == status.HTTP_200_OK
    r = AnimalResponse(**response.json())
    assert r.nombre == updated_animal["nombre"]
    assert r.raza == updated_animal["raza"]
    assert r.edad == updated_animal["edad"]


def test_delete_animal(rest_api):
    """🗑️ Test deleting animal records."""
    # First, create a new animal
    new_animal = {
        "nombre": "Firulais",
        "raza": "Pastor Alemán",
        "edad": 5,
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=new_animal,
    )
    assert response.status_code == status.HTTP_201_CREATED
    animal_id = response.json()["id"]

    # Delete the animal
    response = rest_api.delete(f"{BASE_PATH}/{animal_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the animal has been deleted from the database
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_animal_validation(rest_api):
    """🔍 Test validation of animal inputs."""
    # We cannot create an animal with an empty name
    invalid_animal = {
        "nombre": "",
        "raza": "Pastor Alemán",
        "edad": 5,
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=invalid_animal,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "nombre"]
    # Verificamos que el mensaje de error contenga "field required" en lugar de ser exactamente igual
    assert "field required" in r["detail"][0]["msg"]

    # We cannot create an animal with a negative age
    invalid_animal = {
        "nombre": "Firulais",
        "raza": "Pastor Alemán",
        "edad": -1,
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=invalid_animal,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "edad"]
    assert "greater than or equal to 0" in r["detail"][0]["msg"]

    # We cannot create an animal with a non-integer age
    invalid_animal = {
        "nombre": "Firulais",
        "raza": "Pastor Alemán",
        "edad": "cinco",
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=invalid_animal,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "edad"]
    assert "valid integer" in r["detail"][0]["msg"]

    # We cannot create an animal with an empty breed
    invalid_animal = {
        "nombre": "Firulais",
        "raza": "",
        "edad": 5,
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=invalid_animal,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "raza"]
    assert "field required" in r["detail"][0]["msg"]
