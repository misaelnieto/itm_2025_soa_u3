"""# 🧪 Test Suite for Ventas API.

Este módulo contiene pruebas para los endpoints de la API de ventas. Valida lo siguiente:
- ✅ El comportamiento de la API cuando la base de datos de ventas está vacía.
- 📊 Operaciones CRUD para ventas.
- 🔍 Validación de datos de entrada para ventas.

"""

from fastapi import status

BASE_PATH = "/api/v1/jcontreras/ventas"


def test_empty_database(rest_api):
    """🗃️ Prueba la API con una base de datos vacía."""
    response = rest_api.get(f"{BASE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_venta_with_non_numeric_id(rest_api):
    """🔍 Prueba que GET con un ID no numérico devuelva un error de validación."""
    response = rest_api.get(f"{BASE_PATH}/abc")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_crud_ventas(rest_api):
    """📊 Prueba la API para crear, actualizar, eliminar y obtener ventas."""
    response = rest_api.post(
        f"{BASE_PATH}",
        json={
            "cliente": "Juan Pérez",
            "producto": "Laptop Gamer",
            "cantidad": 2,
            "precio": 35000.00,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["cliente"] == "Juan Pérez"
    assert response_data["producto"] == "Laptop Gamer"
    assert response_data["cantidad"] == 2
    assert response_data["precio"] == 35000.00

    # Obtener venta por ID
    response = rest_api.get(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_200_OK

    # Obtener lista de ventas
    response = rest_api.get(f"{BASE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

    # Obtener una venta que no existe
    response = rest_api.get(f"{BASE_PATH}/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Venta no encontrada."

    # Actualizar una venta
    response = rest_api.put(
        f"{BASE_PATH}/{response_data['id']}",
        json={
            "cliente": "María López",
            "producto": "Monitor 4K",
            "cantidad": 1,
            "precio": 8000.00,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["cliente"] == "María López"
    assert response_data["producto"] == "Monitor 4K"
    assert response_data["cantidad"] == 1
    assert response_data["precio"] == 8000.00

    # Intentar actualizar una venta que no existe
    response = rest_api.put(
        f"{BASE_PATH}/100",
        json={
            "cliente": "Carlos Sánchez",
            "producto": "Teclado Mecánico",
            "cantidad": 1,
            "precio": 2000.00,
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Eliminar una venta
    response = rest_api.delete(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Intentar eliminar una venta que no existe
    response = rest_api.delete(f"{BASE_PATH}/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND
