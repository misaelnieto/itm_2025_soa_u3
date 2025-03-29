# Registro de Ciudades

Este proyecto implementa un sistema de registro y gestión de ciudades utilizando FastAPI. Proporciona una API REST para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre las ciudades, así como funcionalidades adicionales como el cálculo de la población total.

## Endpoints

### 1. Listar Ciudades

**GET** `/registro_ciudades/ciudades`

- **Descripción**: Retorna una lista de todas las ciudades registradas.
- **Respuesta**: Lista de objetos `City`.

---

### 2. Registrar Ciudad

**POST** `/registro_ciudades/registro/{tipo}`

- **Descripción**: Registra una nueva ciudad con un tipo de operación (`entrada` o `salida`).
- **Parámetros**:
  - `tipo`: Tipo de operación (`entrada` para sumar población, `salida` para restar población).
  - `request`: Objeto `CityCreate` con los datos de la ciudad.
- **Validaciones**:
  - Si el tipo es `salida` y la población a restar supera la población total, se rechaza la operación.
- **Respuesta**: Objeto `CityResponse` con el resultado de la operación.

---

### 3. Crear Ciudad

**POST** `/registro_ciudades/ciudades`

- **Descripción**: Crea una nueva ciudad en la base de datos.
- **Parámetros**:
  - `request`: Objeto `CityCreate` con los datos de la ciudad.
- **Validaciones**:
  - El campo `country` no puede estar vacío o contener solo espacios.
- **Respuesta**: Diccionario con los datos de la ciudad creada.

---

### 4. Actualizar Ciudad

**PUT** `/registro_ciudades/actualizar/{city_id}`

- **Descripción**: Actualiza los datos de una ciudad existente.
- **Parámetros**:
  - `city_id`: Identificador de la ciudad.
  - `request`: Objeto `CityUpdate` con los nuevos datos.
- **Validaciones**:
  - Si la ciudad no existe, se retorna un error 404.
- **Respuesta**: Diccionario con los datos actualizados de la ciudad.

---

### 5. Obtener Ciudad

**GET** `/registro_ciudades/ciudades/{city_id}`

- **Descripción**: Obtiene los datos de una ciudad por su identificador.
- **Parámetros**:
  - `city_id`: Identificador de la ciudad.
- **Validaciones**:
  - Si la ciudad no existe, se retorna un error 404.
- **Respuesta**: Diccionario con los datos de la ciudad.

---

### 6. Eliminar Ciudad

**DELETE** `/registro_ciudades/eliminar/{city_id}`

- **Descripción**: Elimina una ciudad de la base de datos.
- **Parámetros**:
  - `city_id`: Identificador de la ciudad.
- **Validaciones**:
  - Si la ciudad no existe, se retorna un error 404.
- **Respuesta**: Objeto `DeleteResponse` con un mensaje de confirmación.

---

## Modelos de Datos

### CityCreate

- `name`: Nombre de la ciudad.
- `population`: Población de la ciudad.
- `country`: País de la ciudad.
- `region`: Región de la ciudad.

### CityUpdate

- `name`: Nombre de la ciudad.
- `population`: Población de la ciudad.
- `country`: País de la ciudad.
- `region`: Región de la ciudad.

### CityResponse

- `result`: Resultado de la operación (`registrado`).
- `previous_population`: Población total antes de la operación.
- `population`: Población total después de la operación.

### DeleteResponse

- `message`: Mensaje de confirmación de eliminación.

---

## Instalación y Ejecución

1. Clona el repositorio.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Ejecuta el servidor con `uvicorn app.proyectos.jheredia.routes:api_router --reload`.
4. Accede a la documentación interactiva en `http://127.0.0.1:8000/docs`.

---

## Pruebas

Ejecuta las pruebas con:

```bash
pytest tests/
```

Asegúrate de cubrir los casos de validación, como campos vacíos o identificadores inexistentes.

---

## Contribuciones

Si deseas contribuir, por favor abre un issue o envía un pull request con tus cambios.

```markdown

```
