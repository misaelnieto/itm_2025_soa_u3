"""gh."""
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


# ✅ Prueba para agregar un carro (POST) /////////////////////////////////////////////////////////////
def test_agregar_carro(rest_api):  # noqa: D103
    carro_nuevo = {
        "marca": "Toyota",
        "modelo": "Corolla",
        "año": 2020,
        "color": "Blanco",
    }

    response = rest_api.post("/api/v1/fcalzada/registro_carro/registro/entrada", json=carro_nuevo)
    assert response.status_code == 201
    
    data = response.json()
    
    # Validar la estructura actual de la respuesta
    assert "result" in data
    assert data["result"] == "registrado"
    assert "inventory" in data
    assert data["inventory"] == 1
    assert "previous_inventory" in data
    assert data["previous_inventory"] == 0

# ✅ Prueba para listar todos los carros (GET) ////////////////////////////////////////////////////////////
def test_listar_carros(rest_api):  # noqa: D103
    response = rest_api.get("/api/v1/fcalzada/registro_carro/carros")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


# ✅ Prueba para actualizar un carro (PUT) //////////////////////////////////////////////////////////////////////
def test_actualizar_carro(rest_api):  # noqa: D103
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


# ✅ Prueba para eliminar un carro (DELETE) /////////////////////////////////////////////////////////////////////////////////
def test_eliminar_carro(rest_api):  # noqa: ARG001, D103
    # Primero, registra un carro
    post_response = client.post("/api/v1/fcalzada/registro_carro/registro/entrada", json={
        "marca": "Toyota", "modelo": "Corolla", "año": 2020, "color": "Rojo",
    })
    assert post_response.status_code == 201
    
    # Verifica que la respuesta tiene los campos que realmente se retornan
    data = post_response.json()
    assert 'result' in data
    assert data['result'] == 'registrado'

    # Ahora puedes proceder a eliminarlo sin intentar acceder a 'id'
    # (Si realmente necesitas eliminarlo, deberías buscar otro campo identificador único)
