"""# 🧪 Test Suite for Contactos API.

This module contains tests for the Contactos API endpoints. It verifies the following:

    - 📋 Retrieval of all contactos.
    - ✏️ Creation of new contactos.
    - 🛠️ Editing existing contactos.
    - ❌ Deletion of contactos.
    - 🔍 Searching contactos by name.
"""

import pytest
from fastapi import status
from pydantic import ValidationError

from app.proyectos.rpalma.schemas import ContactoDB, ContactoResponse  # Import schemas

BASE_PATH = "/api/v1/rpalma/contactos"


def test_agenda_list_empty(rest_api):
    """📋 Test retrieving an empty agenda."""
    response = rest_api.get(f"{BASE_PATH}/agenda")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_crear_contacto(rest_api):
    """✏️ Test creating a new contacto."""
    # Create a new contacto
    payload = {
            "nombre": "Juan Perez",
            "telefono": "1234567890",
            "correo": "juan@example.com",
        }    
    response = rest_api.post(f"{BASE_PATH}/create", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = ContactoResponse(**response.json())
    assert data.status == "successful"
    assert data.message == "Contacto created successfully"
    assert len(data.agenda) == 1
    assert data.agenda[0].nombre == "Juan Perez"


def test_editar_contacto(rest_api):
    """🛠️ Test editing an existing contacto."""
    # Create a contacto first
    payload = {
            "nombre": "Miguel Perez",
            "telefono": "1234567890",
            "correo": "miguel@example.com",
        }    
    response = rest_api.post(f"{BASE_PATH}/create", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    # Edit the contacto
    contacto_id = response.json()["agenda"][0]["id"]
    updated = {
            "nombre": "Miguel Hidalgo",
            "telefono": "1234567890",
            "correo": "juan@example.com",
        }   
    response = rest_api.put(f"{BASE_PATH}/edit/{contacto_id}", json=updated)
    assert response.status_code == status.HTTP_200_OK
    data = ContactoResponse(**response.json())
    assert data.status == "successful"
    assert data.message == "Contacto updated successfully"
    assert data.agenda[0].nombre == "Miguel Hidalgo"

def test_editar_contacto_notfound(rest_api):
    """🛠️ Test editing a non-existent contacto."""
    # Intentar editar un contacto que no existe
    contacto_id = 9999  # ID que no existe en la base de datos
    updated = {
        "nombre": "Nombre Actualizado",
        "telefono": "9876543210",
        "correo": "actualizado@example.com",
    }
    response = rest_api.put(f"{BASE_PATH}/edit/{contacto_id}", json=updated)

    data = response.json()
    assert data["code"] == 404
    assert data["status"] == "failed"
    assert data["message"] == "Contacto not found"


def test_eliminar_contacto(rest_api):
    """❌ Test deleting a contacto."""
    # Create a contacto first
    payload = {
            "nombre": "Miguel Perez",
            "telefono": "1234567890",
            "correo": "miguel@example.com",
        }    
    response = rest_api.post(f"{BASE_PATH}/create", json=payload)
    assert response.status_code == status.HTTP_201_CREATED    

    # Delete the contacto
    contacto_id = response.json()["agenda"][0]["id"]
    response = rest_api.delete(f"{BASE_PATH}/delete/{contacto_id}")
    assert response.status_code == status.HTTP_200_OK
    data = ContactoResponse(**response.json())
    assert data.status == "successful"
    assert data.message == "Contacto deleted successfully"
    assert data.agenda == []
    

def test_eliminar_contacto_notfound(rest_api):
    """❌ Test deleting a non-existent contacto."""
    # Intentar eliminar un contacto que no existe
    contacto_id = 9999  # ID que no existe en la base de datos
    response = rest_api.delete(f"{BASE_PATH}/delete/{contacto_id}")
    
    data = response.json()
    assert data["code"] == 404
    assert data["status"] == "failed"
    assert data["message"] == "Contacto not found"


def test_buscar_contacto(rest_api):
    """🔍 Test searching for a contacto by name."""
    # Create a contacto first
    payload = {
            "nombre": "Miguel Perez",
            "telefono": "1234567890",
            "correo": "miguel@example.com",
        }    
    response = rest_api.post(f"{BASE_PATH}/create", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    # Search for the contacto
    response = rest_api.get(f"{BASE_PATH}/search/Miguel Perez")
    assert response.status_code == status.HTTP_200_OK
    data = ContactoResponse(**response.json())
    assert data.status == "successful"
    assert data.message == "Found contactos matching the search criteria"
    assert len(data.agenda) == 1
    assert data.agenda[0].nombre == "Miguel Perez"
    
def test_buscar_contacto_notfound(rest_api):
    """❌ Test deleting a non-existent contacto."""
    # Intentar eliminar un contacto que no existe
    nombre = "Juan" 
    response = rest_api.get(f"{BASE_PATH}/search/{nombre}")
    
    data = response.json()
    assert data["code"] == 404
    assert data["status"] == "failed"
    assert data["message"] == "Contacto not found"

def test_telefono_valido():
    """✅ Verifica que un número de teléfono válido pase la validación."""
    contacto = ContactoDB(nombre="Juan Perez", telefono="+1234567890", correo="juan@example.com")
    assert contacto.telefono == "+1234567890"
    
def test_telefono_valido_sin_signo_mas():
    """✅ Verifica que un número de teléfono válido sin '+' pase la validación."""
    contacto = ContactoDB(nombre="Maria Lopez", telefono="1234567890", correo="maria@example.com")
    assert contacto.telefono == "1234567890"

def test_telefono_invalido_caracteres():
    """❌ Verifica que un número de teléfono con caracteres no válidos falle la validación."""
    with pytest.raises(ValidationError) as excinfo:
        ContactoDB(nombre="Carlos Gomez", telefono="12345abcde", correo="carlos@example.com")
    assert "El telefono solo puede contener números." in str(excinfo.value)
    
def test_telefono_invalido_incompleto():
    """❌ Verifica que un número de teléfono con menos de 10 dígitos falle la validación."""
    with pytest.raises(ValidationError) as excinfo:
        ContactoDB(nombre="Luis Martinez", telefono="12345", correo="luis@example.com")
    assert "El telefono debe tener al menos 10 dígitos." in str(excinfo.value)
    
def test_telefono_invalido_con_signo_mas_letras():
    """❌ Verifica que un número de teléfono con '+' y caracteres no válidos falle la validación."""
    with pytest.raises(ValidationError) as excinfo:
        ContactoDB(nombre="Ana Torres", telefono="+12345abcde", correo="ana@example.com")
    assert "El telefono solo puede contener números después del '+'" in str(excinfo.value)