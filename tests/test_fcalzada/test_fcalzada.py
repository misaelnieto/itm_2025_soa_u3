"""Documentacion."""
import pytest
from httpx import ASGITransport, AsyncClient
from itm_2025_soa_u3.app.proyectos.fcalzada.schemas import CarroType

from app.main import app

# Base URL corregida para apuntar al servidor real
BASE_URL = "http://0.0.0.0:8000/api/v1/fcalzada/registro_carro"

BASE_PATH = "/api/v1/fcalzada/"
@pytest.mark.asyncio
async def test_add_car():  # noqa: D103
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post(f"{BASE_PATH}/registro_carro/registro/{CarroType.entrada}", json={
            "marca": "Toyota",
            "modelo": "Corolla",
            "anio": 2020,
            "color": "Rojo",
        })
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_all_cars():  # noqa: D103
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.get("/carros")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_car():  # noqa: D103
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        # Primero agregamos un carro para eliminarlo
        response = await client.post("/registro/entrada", json={
            "marca": "Ford",
            "modelo": "Fiesta",
            "anio": 2019,
            "color": "Azul",
        })
        assert response.status_code == 200
        carro_id = response.json()["id"]

        # Ahora lo eliminamos
        delete_response = await client.delete(f"/eliminar/{carro_id}")
        assert delete_response.status_code == 200

@pytest.mark.asyncio
async def test_update_car():  # noqa: D103
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        # Primero agregamos un carro para actualizarlo
        response = await client.post("/registro/entrada", json={
            "marca": "Honda",
            "modelo": "Civic",
            "anio": 2021,
            "color": "Negro",
        })
        assert response.status_code == 200
        carro_id = response.json()["id"]

        # Ahora lo actualizamos
        update_response = await client.put(f"/actualizar/{carro_id}", json={
            "marca": "Honda",
            "modelo": "Accord",
            "anio": 2022,
            "color": "Blanco",
        })
        assert update_response.status_code == 200
