"""# 🧪 Test Suite for Alcancia API.

This module contains tests for the Alcancia API endpoints. It verifies the following:
- ✅ The behavior of the API when the database is empty.
- 💰 Creation of products.
- 🔍 Validation of input data for products.
"""

from fastapi import status

BASE_PATH = "/api/v1/dramos/productos"


def test_empty_database(rest_api):
    """🗃️ Tests the API with an empty database."""
    response = rest_api.get(f"{BASE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    response = rest_api.post(
        f"{BASE_PATH}",
        json={
            "nombre": "Coca-Cola",
            "tipo": "Refresco",
            "precio": 15,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["nombre"] == "Coca-Cola"
    assert response_data["tipo"] == "Refresco"
    assert response_data["precio"] == 15

    response = rest_api.get(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_200_OK

    response = rest_api.get(f"{BASE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

    response = rest_api.get(f"{BASE_PATH}/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Producto no encontrado."

    response = rest_api.put(
        f"{BASE_PATH}/{response_data['id']}",
        json={
            "nombre": "Jumex",
            "tipo": "Tipo Actualizado",
            "precio": 17,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["nombre"] == "Jumex"
    assert response_data["tipo"] == "Tipo Actualizado"
    assert response_data["precio"] == 17

    response = rest_api.put(
        f"{BASE_PATH}/100",
        json={
            "nombre": "Jumex",
            "tipo": "Tipo Actualizado",
            "precio": 17,
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Producto no encontrado"

    response = rest_api.delete(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = rest_api.delete(f"{BASE_PATH}/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND