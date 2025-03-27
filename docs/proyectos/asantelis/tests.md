# 🧪 Documentación de Pruebas

Esta sección contiene la documentación detallada de las pruebas automatizadas para el API de Registro de Animales.

## 🔬 Pruebas del Backend

Las pruebas automatizadas del backend se encuentran en el archivo `/tests/test_asantelis.py`. Estas pruebas verifican el correcto funcionamiento de las rutas y la lógica de negocio del API.

### 🗃️ test_empty_database

```python
def test_empty_database(rest_api):
    """🗃️ Tests the API with an empty database."""
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
```

Esta prueba verifica que la API responda correctamente cuando la base de datos está vacía. Comprueba que:
- La ruta `GET /animales` responda con un código de estado 200 (OK).
- La respuesta sea una lista vacía.

### 🐾 test_create_animal

```python
def test_create_animal(rest_api):
    """🐾 Test creating animal records."""
    # First, the database is empty
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    # Now let's create a new animal
    new_animal = {"nombre": "Firulais", "raza": "Pastor Alemán", "edad": 5}
    response = rest_api.post(f"{BASE_PATH}/", json=new_animal)
    assert response.status_code == status.HTTP_201_CREATED
    r = AnimalResponse(**response.json())
    assert r.nombre == new_animal["nombre"]
    assert r.raza == new_animal["raza"]
    assert r.edad == new_animal["edad"]

    # Verify the animal is in the database
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    animals = response.json()
    assert len(animals) == 1
    assert animals[0]["nombre"] == new_animal["nombre"]
    assert animals[0]["raza"] == new_animal["raza"]
    assert animals[0]["edad"] == new_animal["edad"]
```

Esta prueba verifica la funcionalidad de creación de un nuevo animal. Comprueba que:
1. ✅ Inicialmente, la base de datos está vacía.
2. ✅ Se puede crear un nuevo animal con datos válidos.
3. ✅ La respuesta de creación contiene los datos correctos del animal.
4. ✅ Después de la creación, el animal aparece en la lista de animales.

### ✏️ test_update_animal

```python
def test_update_animal(rest_api):
    """✏️ Test updating animal records."""
    # First, create a new animal
    new_animal = {"nombre": "Firulais", "raza": "Pastor Alemán", "edad": 5}
    response = rest_api.post(f"{BASE_PATH}/", json=new_animal)
    assert response.status_code == status.HTTP_201_CREATED
    animal_id = response.json()["id"]

    # Update the animal's details
    updated_animal = {"nombre": "Max", "raza": "Labrador", "edad": 6}
    response = rest_api.put(f"{BASE_PATH}/{animal_id}", json=updated_animal)
    assert response.status_code == status.HTTP_200_OK
    r = AnimalResponse(**response.json())
    assert r.nombre == updated_animal["nombre"]
    assert r.raza == updated_animal["raza"]
    assert r.edad == updated_animal["edad"]

    # Verify the animal's details have been updated in the database
    response = rest_api.get(f"{BASE_PATH}/{animal_id}")
    assert response.status_code == status.HTTP_200_OK
    r = AnimalResponse(**response.json())
    assert r.nombre == updated_animal["nombre"]
    assert r.raza == updated_animal["raza"]
    assert r.edad == updated_animal["edad"]
```

Esta prueba verifica la funcionalidad de actualización de un animal existente. Comprueba que:
1. ✅ Se puede crear un nuevo animal para la prueba.
2. ✅ Se pueden actualizar los detalles del animal.
3. ✅ La respuesta de actualización contiene los datos actualizados.
4. ✅ Los cambios se reflejan correctamente en la base de datos.

### 🗑️ test_delete_animal

```python
def test_delete_animal(rest_api):
    """🗑️ Test deleting animal records."""
    # First, create a new animal
    new_animal = {
        "nombre": "Firulais",
        "raza": "Pastor Alemán",
        "edad": 5,
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=new_animal,
    )
    assert response.status_code == status.HTTP_201_CREATED
    animal_id = response.json()["id"]

    # Delete the animal
    response = rest_api.delete(f"{BASE_PATH}/{animal_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the animal has been deleted from the database
    response = rest_api.get(f"{BASE_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
```

Esta prueba verifica la funcionalidad de eliminación de un animal. Comprueba que:
1. ✅ Se puede crear un nuevo animal para la prueba.
2. ✅ Se puede eliminar el animal correctamente.
3. ✅ Después de la eliminación, la lista de animales está vacía.

### 🔍 test_animal_validation

```python
def test_animal_validation(rest_api):
    """🔍 Test validation of animal inputs."""
    # We cannot create an animal with an empty name
    invalid_animal = {
        "nombre": "",
        "raza": "Pastor Alemán",
        "edad": 5,
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=invalid_animal,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "nombre"]
    assert "field required" in r["detail"][0]["msg"]

    # We cannot create an animal with a negative age
    invalid_animal = {
        "nombre": "Firulais",
        "raza": "Pastor Alemán",
        "edad": -1,
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=invalid_animal,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "edad"]
    assert "greater than or equal to 0" in r["detail"][0]["msg"]

    # We cannot create an animal with a non-integer age
    invalid_animal = {
        "nombre": "Firulais",
        "raza": "Pastor Alemán",
        "edad": "cinco",
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=invalid_animal,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "edad"]
    assert "valid integer" in r["detail"][0]["msg"]

    # We cannot create an animal with an empty breed
    invalid_animal = {
        "nombre": "Firulais",
        "raza": "",
        "edad": 5,
    }
    response = rest_api.post(
        f"{BASE_PATH}/",
        json=invalid_animal,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    r = response.json()
    assert r["detail"][0]["loc"] == ["body", "raza"]
    assert "field required" in r["detail"][0]["msg"]
```

Esta prueba verifica las validaciones de datos para la creación de animales. Comprueba que:
1. ❌ No se puede crear un animal con un nombre vacío.
2. ❌ No se puede crear un animal con una edad negativa.
3. ❌ No se puede crear un animal con una edad no numérica.
4. ❌ No se puede crear un animal con una raza vacía.

## 🚀 Ejecución de Pruebas

Para ejecutar todas las pruebas, utiliza el siguiente comando:

```bash
uv run pytest
```

Para ejecutar solo las pruebas del API de animales, utiliza:

```bash
uv run pytest tests/test_asantelis.py -v
```

El flag `-v` (verbose) muestra información detallada sobre cada prueba ejecutada.
