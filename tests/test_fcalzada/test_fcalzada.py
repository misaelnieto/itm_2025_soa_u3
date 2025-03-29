"""gh."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

# Cliente para simular las solicitudes HTTP
client = TestClient(app)

# Datos de prueba
carro_nuevo = {
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2020,
    "color": "Rojo",
}

carro_actualizado = {
    "marca": "Honda",
    "modelo": "Civic",
    "año": 2022,
    "color": "Negro",
}


# ✅ Prueba para agregar un carro (POST)
def test_agregar_carro(rest_api):
    response = rest_api.post("/api/v1/fcalzada/registro_carro/registro/entrada", json=carro_nuevo)
    assert response.status_code == 201
    data = response.json()
    assert data["marca"] == carro_nuevo["marca"]
    assert data["modelo"] == carro_nuevo["modelo"]
    assert data["año"] == carro_nuevo["año"]
    assert data["color"] == carro_nuevo["color"]


# ✅ Prueba para listar todos los carros (GET)
def test_listar_carros(rest_api):
    response = rest_api.get("/api/v1/fcalzada/registro_carro/carros")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


# ✅ Prueba para actualizar un carro (PUT)
def test_actualizar_carro(rest_api):
    # Primero, agregamos un carro para obtener su ID
    post_response = rest_api.post("/api/v1/fcalzada/registro_carro/registro/normal", json=carro_nuevo)
    carro_id = post_response.json()["id"]

    # Actualizamos ese carro
    put_response = rest_api.put(f"/api/v1/fcalzada/registro_carro/actualizar/{carro_id}", json=carro_actualizado)
    assert put_response.status_code == 200
    data = put_response.json()
    assert data["marca"] == carro_actualizado["marca"]
    assert data["modelo"] == carro_actualizado["modelo"]
    assert data["año"] == carro_actualizado["año"]
    assert data["color"] == carro_actualizado["color"]


# ✅ Prueba para eliminar un carro (DELETE)
def test_eliminar_carro(rest_api):
    # Primero, agregamos un carro para obtener su ID
    post_response = rest_api.post("/api/v1/fcalzada/registro_carro/registro/normal", json=carro_nuevo)
    carro_id = post_response.json()["id"]

    # Eliminamos el carro
    delete_response = rest_api.delete(f"/api/v1/fcalzada/registro_carro/eliminar/{carro_id}")
    assert delete_response.status_code == 200

    # Verificamos que ya no existe
    get_response = rest_api.get(f"/api/v1/fcalzada/registro_carro/carros")
    assert all(carro["id"] != carro_id for carro in get_response.json())
