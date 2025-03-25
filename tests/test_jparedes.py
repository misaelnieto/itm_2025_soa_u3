"""# 🧪 Test Suite for Alcancia API.

This module contains tests for the Alcancia API endpoints. It verifies the following:
- ✅ The behavior of the API when the database is empty.
- 💰 Deposit transactions.
- 💸 Withdrawal transactions.
- 🔍 Validation of input data for transactions.
"""

from datetime import datetime  # Add this import

from fastapi import status

from app.proyectos.jparedes.schemas import TransactionBase

BASE_PATH = "/api/v1/jparedes/libros"


def test_empty_database(rest_api):
    """🗃️ Tests the API with an empty database."""
    response = rest_api.get(f"{BASE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_crud_books(rest_api):
    """📚 Tests the API to create a new book."""
    response = rest_api.post(
        f"{BASE_PATH}",
        json={
            "isbn": 1234567890,
            "titulo": "Libro de Prueba",
            "autor": "Autor de Prueba",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["isbn"] == 1234567890
    assert response_data["titulo"] == "Libro de Prueba"
    assert response_data["autor"] == "Autor de Prueba"

    # Get book by id
    response = rest_api.get(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_200_OK

    # Get List of books
    response = rest_api.get(f"{BASE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

    # Get a book that does not exist
    response = rest_api.get(f"{BASE_PATH}/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Libro no encontrado."

    # Update a book
    response = rest_api.put(
        f"{BASE_PATH}/{response_data['id']}",
        json={
            "isbn": 1234567890,
            "titulo": "Libro Actualizado",
            "autor": "Autor Actualizado",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["isbn"] == 1234567890
    assert response_data["titulo"] == "Libro Actualizado"
    assert response_data["autor"] == "Autor Actualizado"

    # Update a book that does not exist
    response = rest_api.put(
        f"{BASE_PATH}/100",
        json={
            "isbn": 1234567890,
            "titulo": "Libro Actualizado",
            "autor": "Autor Actualizado",
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Delete a book
    response = rest_api.delete(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Delete a book that does not exist
    response = rest_api.delete(f"{BASE_PATH}/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND
