"""#Test Suite for Courses API.

This module contains tests for the Courses API endpoints. It verifies the following:
- The behavior of the API when the database is empty.
- Create courses records.
- Update courses records.
- Delete courses records.
- Validation of input data for courses records.
"""

from fastapi import status

from app.proyectos.jchaidez.schemas import CourseResponse

BASE_PATH = "/api/v1/jchaidez/cursos"


def test_empty_database(rest_api):
    """Tests the API with an empty database."""
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_curso(rest_api):
    """Test creating course records."""
    # Empty database
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    # Create a new course
    new_curso = {"nombre": "Introducción a Python", "descripcion": "Curso básico de programación en Python.", "maestro": "Noe Nieto"}
    response = rest_api.post(f"{BASE_PATH}/", json=new_curso)
    assert response.status_code == status.HTTP_201_CREATED
    r = CourseResponse(**response.json())
    assert r.nombre == new_curso["nombre"]
    assert r.descripcion == new_curso["descripcion"]
    assert r.maestro == new_curso["maestro"]

    # Verify the course is in the database
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    courses = response.json()
    assert len(courses) == 1
    assert courses[0]["nombre"] == new_curso["nombre"]
    assert courses[0]["descripcion"] == new_curso["descripcion"]
    assert courses[0]["maestro"] == new_curso["maestro"]


def test_update_curso(rest_api):
    """Test updating course records."""
    # Create a new course
    new_curso = {"nombre": "Introducción a Python", "descripcion": "Curso básico de programación en Python.", "maestro": "Noe Nieto"}
    response = rest_api.post(f"{BASE_PATH}/", json=new_curso)
    assert response.status_code == status.HTTP_201_CREATED
    curso_id = response.json()["id"]

    # Update the course's details
    updated_curso = {"nombre": "Python avanzado", "descripcion": "Curso avanzado de programación en Python.", "maestro": "Noe Nieto"}
    response = rest_api.put(f"{BASE_PATH}/{curso_id}", json=updated_curso)
    assert response.status_code == status.HTTP_200_OK
    r = CourseResponse(**response.json())
    assert r.nombre == updated_curso["nombre"]
    assert r.descripcion == updated_curso["descripcion"]
    assert r.maestro == updated_curso["maestro"]

    # Verify the course's details have been updated in the database
    response = rest_api.get(f"{BASE_PATH}/{curso_id}")
    assert response.status_code == status.HTTP_200_OK
    r = CourseResponse(**response.json())
    assert r.nombre == updated_curso["nombre"]
    assert r.descripcion == updated_curso["descripcion"]
    assert r.maestro == updated_curso["maestro"]

    # Update course that does not exist
    response = rest_api.put(f"{BASE_PATH}/1000", json=updated_curso)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Update course with an empty field
    updated_curso = {"nombre": "Python avanzado", "descripcion": " ", "maestro": "Noe Nieto"}
    response = rest_api.put(f"{BASE_PATH}/{curso_id}", json=updated_curso)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_curso(rest_api):
    """Test deleting course records."""
    # Create a new course
    new_curso = {
        "nombre": "Introducción a Python",
        "descripcion": "Curso básico de programación en Python.",
        "maestro": "Noe Nieto",
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=new_curso,
    )
    assert response.status_code == status.HTTP_201_CREATED
    curso_id = response.json()["id"]

    # Delete the course
    response = rest_api.delete(f"{BASE_PATH}/{curso_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the course has been deleted from the database
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    # Delete course that does not exist
    response = rest_api.delete(f"{BASE_PATH}/1000")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_curso_validation(rest_api):
    """Test validation of course inputs."""
    # Cannot create an course with an empty name
    invalid_curso = {
        "nombre": "",
        "descripcion": "Curso básico de programación en Python.",
        "maestro": "Noe Nieto",
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=invalid_curso,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "nombre"]
    # the error message contains 'field required'
    assert "Campo requerido" in r["detail"][0]["msg"]

    # Cannot create an course with an empty description
    invalid_curso = {
        "nombre": "Introducción a Python",
        "descripcion": "",
        "maestro": "Noe Nieto",
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=invalid_curso,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "descripcion"]
    assert "Campo requerido" in r["detail"][0]["msg"]
    
    # Cannot create an course with an empty maestro
    invalid_curso = {
        "nombre": "Introducción a Python",
        "descripcion": "Curso básico de programación en Python.",
        "maestro": "",
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=invalid_curso,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "maestro"]
    assert "Campo requerido" in r["detail"][0]["msg"]

    # Get course that does not exist
    response = rest_api.get(f"{BASE_PATH}/1000")
    assert response.status_code == status.HTTP_404_NOT_FOUND