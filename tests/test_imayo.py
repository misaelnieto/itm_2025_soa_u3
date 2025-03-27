# 🎟️ Test Suite para la API de Eventos.

"""Este módulo contiene pruebas para los endpoints de la API de eventos. Se verifican los siguientes casos:
- 🗃️ Comprobación de la API con una base de datos vacía.
- 🎟️ Creación de eventos.
- 📜 Recuperación de eventos.
- ✏️ Actualización de eventos.
- ❌ Eliminación de eventos.
"""  # noqa: D205

from fastapi import status

# Definición del prefijo base para las rutas de la API de eventos
BASE_PATH = "/api/v1/imayo/eventos"

def test_empty_database(rest_api):
    """🗃️ Prueba la API con una base de datos vacía."""
    response = rest_api.get(f"{BASE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []  # La respuesta debe ser una lista vacía


def test_crud_events(rest_api):
    """🎟️ Prueba el CRUD de eventos en la API."""
    # 📌 Crear un evento
    response = rest_api.post(
        f"{BASE_PATH}",
        json={
            "nombre": "Evento de Prueba",
            "descripcion": "Descripción del evento de prueba",
            "fecha": "2025-06-15T10:00:00",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()

    # Verifica que los datos del evento creado sean correctos
    assert response_data["id"] == 1
    assert response_data["nombre"] == "Evento de Prueba"
    assert response_data["descripcion"] == "Descripción del evento de prueba"
    assert response_data["fecha"] == "2025-06-15T10:00:00"

    # 📌 Obtener evento por ID
    response = rest_api.get(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_200_OK

    # 📌 Obtener la lista de eventos
    response = rest_api.get(f"{BASE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1  # Debe haber un evento registrado

    # 📌 Intentar obtener un evento que no existe
    response = rest_api.get(f"{BASE_PATH}/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Evento no encontrado."

    # 📌 Actualizar un evento existente
    response = rest_api.put(
        f"{BASE_PATH}/{response_data['id']}",
        json={
            "nombre": "Evento Actualizado",
            "descripcion": "Descripción actualizada",
            "fecha": "2025-07-20T15:00:00",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    # Verifica que los datos actualizados sean correctos
    assert response_data["id"] == 1
    assert response_data["nombre"] == "Evento Actualizado"
    assert response_data["descripcion"] == "Descripción actualizada"
    assert response_data["fecha"] == "2025-07-20T15:00:00"

    # 📌 Intentar actualizar un evento que no existe
    response = rest_api.put(
        f"{BASE_PATH}/100",
        json={
            "nombre": "Evento Actualizado",
            "descripcion": "Descripción actualizada",
            "fecha": "2025-07-20T15:00:00",
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # 📌 Eliminar un evento existente
    response = rest_api.delete(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # 📌 Intentar eliminar un evento que no existe
    response = rest_api.delete(f"{BASE_PATH}/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND
