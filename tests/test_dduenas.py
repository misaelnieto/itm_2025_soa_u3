"""🧪 Test Suite for Student API.

This module contains tests for the Student API endpoints. It verifies the following:
- ✅ The behavior of the API when the database is empty.
- 📚 CRUD operations for students.
"""

from fastapi import status

BASE_PATH = "/api/v1/dduenas/estudiantes"


def test_empty_database(rest_api):
    """🗃️ Tests the API with an empty database."""
    response = rest_api.get(f"{BASE_PATH}")
    assert response.status_code == status.HTTP_200_OK, f"Expected 200 OK, got {response.status_code}"
    assert response.json() == [], f"Expected empty list, got {response.json()}"

def test_crud_students(rest_api):
    """Tests the API to create, update, delete and get list of students."""
    response = rest_api.post(
        f"{BASE_PATH}",
        json={
            "nombre": "Nombre de prueba",
            "carrera":"Carrera de prueba",
            
            
            },
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["nombre"] == "Nombre de prueba"
    assert response_data["carrera"] == "Carrera de prueba"
    
    

    # Obtener un estudiante mediante su id
    response = rest_api.get(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_200_OK

     # Obtener una lista de estudiante
    response = rest_api.get(f"{BASE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

       # Obtener un estudiante que no existe
    response = rest_api.get(f"{BASE_PATH}/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Estudiante no encontrado." 

     # Actualizar un estudiante
    response = rest_api.put(
        f"{BASE_PATH}/{response_data['id']}",
        json={
            "id": 1,
            "nombre": "Nombre Actualizado",
            "carrera": "Carrera Actualizada",
            
        },
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["nombre"] == "Nombre Actualizado"
    assert response_data["carrera"] == "Carrera Actualizada"
    

 # Actualizar un estudiante que no existe
    response = rest_api.put(
        f"{BASE_PATH}/100",
        json={
            "nombre": "Nombre Actualizado",
            "carrera": "Carrera Actualizado",
            
        },  
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

 # Eliminar un estudiante
    response = rest_api.delete(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Eliminar a un estudiante que no existe
    response = rest_api.delete(f"{BASE_PATH}/100")
    assert response.status_code == status.HTTP_404_NOT_FOUND