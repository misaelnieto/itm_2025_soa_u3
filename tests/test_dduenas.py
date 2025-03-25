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
    """📚 Tests the API to create, read, update, and delete a student."""
    # Create a new student
    response = rest_api.post(
        f"{BASE_PATH}",
        json={
            "nombre": "Juan Pérez",
            "carrera": "Ingeniería en Sistemas",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED, f"Expected 201 Created, got {response.status_code}"
    response_data = response.json()
    assert response_data["id"] == 1, f"Expected id 1, got {response_data['id']}"
    assert response_data["nombre"] == "Juan Pérez", f"Expected nombre 'Juan Pérez', got {response_data['nombre']}"
    assert response_data["carrera"] == "Ingeniería en Sistemas", f"Expected carrera 'Ingeniería en Sistemas', got {response_data['carrera']}"

    # Get student by ID
    response = rest_api.get(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_200_OK, f"Expected 200 OK, got {response.status_code}"
    student = response.json()
    assert student["id"] == 1, f"Expected id 1, got {student['id']}"
    assert student["nombre"] == "Juan Pérez", f"Expected nombre 'Juan Pérez', got {student['nombre']}"
    assert student["carrera"] == "Ingeniería en Sistemas", f"Expected carrera 'Ingeniería en Sistemas', got {student['carrera']}"

    # Get all students
    response = rest_api.get(f"{BASE_PATH}")
    assert response.status_code == status.HTTP_200_OK, f"Expected 200 OK, got {response.status_code}"
    students = response.json()
    assert len(students) == 1, f"Expected 1 student, got {len(students)}"

    # Update the student
    response = rest_api.put(
        f"{BASE_PATH}/{response_data['id']}",
        json={
            "nombre": "Juan Pérez Actualizado",
            "carrera": "Ingeniería en Software",
        },
    )
    assert response.status_code == status.HTTP_200_OK, f"Expected 200 OK, got {response.status_code}"
    updated_student = response.json()
    assert updated_student["nombre"] == "Juan Pérez Actualizado", f"Expected nombre 'Juan Pérez Actualizado', got {updated_student['nombre']}"
    assert updated_student["carrera"] == "Ingeniería en Software", f"Expected carrera 'Ingeniería en Software', got {updated_student['carrera']}"

    # Delete the student
    response = rest_api.delete(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, f"Expected 204 No Content, got {response.status_code}"

    # Verify the student was deleted
    response = rest_api.get(f"{BASE_PATH}/{response_data['id']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, f"Expected 404 Not Found, got {response.status_code}"
    assert response.json()["detail"] == "Estudiante no encontrado.", f"Expected 'Estudiante no encontrado.', got {response.json()['detail']}"




