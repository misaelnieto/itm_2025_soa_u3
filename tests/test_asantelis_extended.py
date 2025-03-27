"""# 🧪 Pruebas extendidas para la API de Animales.

Este módulo contiene pruebas adicionales para la API de Animales, enfocándose en:
- 🚫 Casos de error (404, etc.)
- 🔄 Actualizaciones parciales
- ⚙️ Validaciones adicionales
"""

import pytest
from fastapi import status

from app.proyectos.asantelis.models import now_utc
from app.proyectos.asantelis.schemas import AnimalResponse, AnimalUpdate

BASE_PATH = "/api/v1/asantelis/animales"


def test_get_nonexistent_animal(rest_api):
    """🚫 Prueba intentar obtener un animal que no existe."""
    # Intentar obtener un animal con un ID que no existe
    response = rest_api.get(f"{BASE_PATH}/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Animal not found"


def test_update_nonexistent_animal(rest_api):
    """🚫 Prueba intentar actualizar un animal que no existe."""
    # Intentar actualizar un animal con un ID que no existe
    updated_animal = {"nombre": "Max", "raza": "Labrador", "edad": 6}
    response = rest_api.put(f"{BASE_PATH}/999", json=updated_animal)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Animal not found"


def test_delete_nonexistent_animal(rest_api):
    """🚫 Prueba intentar eliminar un animal que no existe."""
    # Intentar eliminar un animal con un ID que no existe
    response = rest_api.delete(f"{BASE_PATH}/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Animal not found"


def test_partial_update_animal(rest_api):
    """🔄 Prueba actualizar parcialmente un animal."""
    # Primero, crear un nuevo animal
    new_animal = {"nombre": "Firulais", "raza": "Pastor Alemán", "edad": 5}
    response = rest_api.post(f"{BASE_PATH}/", json=new_animal)
    assert response.status_code == status.HTTP_201_CREATED
    animal_id = response.json()["id"]

    # Actualizar solo el nombre del animal
    partial_update = {"nombre": "Max"}
    response = rest_api.put(f"{BASE_PATH}/{animal_id}", json=partial_update)
    assert response.status_code == status.HTTP_200_OK
    r = AnimalResponse(**response.json())
    assert r.nombre == "Max"
    assert r.raza == new_animal["raza"]  # No debería cambiar
    assert r.edad == new_animal["edad"]  # No debería cambiar

    # Actualizar solo la raza del animal
    partial_update = {"raza": "Labrador"}
    response = rest_api.put(f"{BASE_PATH}/{animal_id}", json=partial_update)
    assert response.status_code == status.HTTP_200_OK
    r = AnimalResponse(**response.json())
    assert r.nombre == "Max"  # No debería cambiar
    assert r.raza == "Labrador"
    assert r.edad == new_animal["edad"]  # No debería cambiar

    # Actualizar solo la edad del animal
    partial_update = {"edad": 6}
    response = rest_api.put(f"{BASE_PATH}/{animal_id}", json=partial_update)
    assert response.status_code == status.HTTP_200_OK
    r = AnimalResponse(**response.json())
    assert r.nombre == "Max"  # No debería cambiar
    assert r.raza == "Labrador"  # No debería cambiar
    assert r.edad == 6


def test_update_validation(rest_api):
    """⚙️ Prueba la validación de datos en actualizaciones."""
    # Primero, crear un nuevo animal
    new_animal = {"nombre": "Firulais", "raza": "Pastor Alemán", "edad": 5}
    response = rest_api.post(f"{BASE_PATH}/", json=new_animal)
    assert response.status_code == status.HTTP_201_CREATED
    animal_id = response.json()["id"]

    # Intentar actualizar con un nombre vacío
    invalid_update = {"nombre": ""}
    response = rest_api.put(f"{BASE_PATH}/{animal_id}", json=invalid_update)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "nombre"]
    assert "field required" in r["detail"][0]["msg"]

    # Intentar actualizar con una raza vacía
    invalid_update = {"raza": ""}
    response = rest_api.put(f"{BASE_PATH}/{animal_id}", json=invalid_update)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "raza"]
    assert "field required" in r["detail"][0]["msg"]

    # Intentar actualizar con una edad negativa
    invalid_update = {"edad": -1}
    response = rest_api.put(f"{BASE_PATH}/{animal_id}", json=invalid_update)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "edad"]
    assert "greater than or equal to 0" in r["detail"][0]["msg"]
