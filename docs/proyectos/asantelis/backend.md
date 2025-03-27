# 🖥️ Documentación del Backend

Esta sección contiene la documentación detallada de las funciones del backend para el API de Registro de Animales.

## 🔌 Rutas API

El backend expone las siguientes rutas para interactuar con el registro de animales:

### 📜 GET /animales

```python
@api_router.get("/", tags=["Animales"])
def animals_list(db: DbSession) -> list[Register]:
    """Retrieve the list of all registered animals.

    This endpoint returns all animals registered in the application.
    
    - **Returns**: `list[Register]`: A list of all registered animals.
    """
```

Esta función recupera la lista de todos los animales registrados en la base de datos.

**Parámetros:**
- `db`: Sesión de base de datos proporcionada por FastAPI.

**Retorna:**
- Lista de objetos `Register` que representan a todos los animales registrados.

**Ejemplo de respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Firulais",
    "raza": "Pastor Alemán",
    "edad": 5,
    "created_at": "2025-03-13T07:48:04.965275"
  },
  {
    "id": 2,
    "nombre": "Rex",
    "raza": "Bulldog",
    "edad": 3,
    "created_at": "2025-03-14T07:05:07.841158"
  }
]
```

### ➕ POST /animales

```python
@api_router.post("/", tags=["Animales"], status_code=status.HTTP_201_CREATED)
async def create_animal(animal: AnimalCreate, db: DbSession) -> AnimalResponse:
    """Register a new animal.

    This endpoint registers a new animal in the application.

    **Args:**
    - `animal` (`AnimalCreate`): The details of the animal to be registered.

    **Returns:**
    - `AnimalResponse`: The response containing the registered animal details.
    """
```

Esta función registra un nuevo animal en la base de datos.

**Parámetros:**
- `animal`: Objeto `AnimalCreate` con los detalles del animal a registrar.
- `db`: Sesión de base de datos proporcionada por FastAPI.

**Retorna:**
- Objeto `AnimalResponse` con los detalles del animal registrado, incluyendo el ID asignado.

**Ejemplo de solicitud:**
```json
{
  "nombre": "Firulais",
  "raza": "Pastor Alemán",
  "edad": 5
}
```

**Ejemplo de respuesta:**
```json
{
  "id": 1,
  "nombre": "Firulais",
  "raza": "Pastor Alemán",
  "edad": 5,
  "created_at": "2025-03-13T07:48:04.965275"
}
```

### 🔍 GET /animales/{animal_id}

```python
@api_router.get("/{animal_id}", tags=["Animales"])
async def get_animal(animal_id: int, db: DbSession) -> AnimalResponse:
    """Retrieve details of a specific animal.

    This endpoint retrieves the details of a specific animal by its ID.

    **Args:**
    - `animal_id` (`int`): The ID of the animal to be retrieved.

    **Returns:**
    - `AnimalResponse`: The response containing the animal details.

    **Raises:**
    - `HTTPException`: If the animal is not found, a 404 Not Found error is raised.
    """
```

Esta función recupera los detalles de un animal específico por su ID.

**Parámetros:**
- `animal_id`: ID del animal a recuperar.
- `db`: Sesión de base de datos proporcionada por FastAPI.

**Retorna:**
- Objeto `AnimalResponse` con los detalles del animal.

**Excepciones:**
- `HTTPException` con código 404 si el animal no se encuentra.

**Ejemplo de respuesta:**
```json
{
  "id": 1,
  "nombre": "Firulais",
  "raza": "Pastor Alemán",
  "edad": 5,
  "created_at": "2025-03-13T07:48:04.965275"
}
```

### ✏️ PUT /animales/{animal_id}

```python
@api_router.put("/{animal_id}", tags=["Animales"])
async def update_animal(animal_id: int, animal_update: AnimalUpdate, db: DbSession) -> AnimalResponse:
    """Update details of a specific animal.

    This endpoint updates the details of a specific animal by its ID.

    **Args:**
    - `animal_id` (`int`): The ID of the animal to be updated.
    - `animal_update` (`AnimalUpdate`): The updated details of the animal.

    **Returns:**
    - `AnimalResponse`: The response containing the updated animal details.

    **Raises:**
    - `HTTPException`: If the animal is not found, a 404 Not Found error is raised.
    """
```

Esta función actualiza los detalles de un animal específico por su ID.

**Parámetros:**
- `animal_id`: ID del animal a actualizar.
- `animal_update`: Objeto `AnimalUpdate` con los detalles actualizados del animal.
- `db`: Sesión de base de datos proporcionada por FastAPI.

**Retorna:**
- Objeto `AnimalResponse` con los detalles actualizados del animal.

**Excepciones:**
- `HTTPException` con código 404 si el animal no se encuentra.

**Ejemplo de solicitud:**
```json
{
  "nombre": "Max",
  "raza": "Labrador",
  "edad": 6
}
```

**Ejemplo de respuesta:**
```json
{
  "id": 1,
  "nombre": "Max",
  "raza": "Labrador",
  "edad": 6,
  "created_at": "2025-03-13T07:48:04.965275"
}
```

### 🗑️ DELETE /animales/{animal_id}

```python
@api_router.delete("/{animal_id}", tags=["Animales"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_animal(animal_id: int, db: DbSession):
    """Delete a specific animal registration.

    This endpoint deletes a specific animal registration by its ID.

    **Args:**
    - `animal_id` (`int`): The ID of the animal to be deleted.

    **Raises:**
    - `HTTPException`: If the animal is not found, a 404 Not Found error is raised.
    """
```

Esta función elimina el registro de un animal específico por su ID.

**Parámetros:**
- `animal_id`: ID del animal a eliminar.
- `db`: Sesión de base de datos proporcionada por FastAPI.

**Retorna:**
- Respuesta con código 204 (No Content) si la eliminación fue exitosa.

**Excepciones:**
- `HTTPException` con código 404 si el animal no se encuentra.

## 📊 Modelos de Base de Datos

El backend utiliza SQLModel para definir el modelo de datos para los animales:

```python
class Register(SQLModel, table=True):
    """Modelo para registrar los animales en la base de datos."""

    __tablename__ = "animales"  # Nombre de la tabla en la base de datos
    id: int | None = Field(default=None, primary_key=True)  # Identificador único del animal
    nombre: str = Field(title="Nombre", nullable=False)  # Nombre del animal
    raza: str = Field(title="Raza", nullable=False)  # Raza del animal
    edad: int = Field(title="Edad", nullable=False)  # Edad del animal
    created_at: datetime = Field(
        title="Created At",
        default_factory=now_utc,
        nullable=False,
    )
```

Este modelo define la estructura de la tabla `animales` en la base de datos, con los siguientes campos:
- `id`: Identificador único del animal (clave primaria).
- `nombre`: Nombre del animal.
- `raza`: Raza del animal.
- `edad`: Edad del animal.
- `created_at`: Fecha y hora de registro del animal.

## 📝 Esquemas de Validación

El backend utiliza Pydantic para definir esquemas de validación para las operaciones de creación y actualización de animales:

### ➕ AnimalCreate

```python
class AnimalCreate(BaseModel):
    """Schema for creating a new animal."""

    nombre: str
    """The name of the animal"""
    raza: str
    """The breed of the animal"""
    edad: int = Field(..., ge=0)
    """The age of the animal"""

    @field_validator("nombre", "raza", mode="before")
    @classmethod
    def validate_not_empty(cls, v):
        """Valida que los campos de texto no estén vacíos."""
        if not v or v.strip() == "":
            raise ValueError("field required")
        return v
```

Este esquema define la estructura de datos para crear un nuevo animal, con validaciones para asegurar que:
- `nombre` y `raza` no estén vacíos.
- `edad` sea un número entero mayor o igual a 0.

### ✏️ AnimalUpdate

```python
class AnimalUpdate(BaseModel):
    """Schema for updating an existing animal."""

    nombre: Optional[str] = None
    """The name of the animal"""
    raza: Optional[str] = None
    """The breed of the animal"""
    edad: Optional[int] = Field(None, ge=0)
    """The age of the animal"""

    @field_validator("nombre", "raza")
    @classmethod
    def validate_not_empty(cls, v):
        """Valida que los campos de texto no estén vacíos si se proporcionan."""
        if v is not None and (not v or v.strip() == ""):
            raise ValueError("field required")
        return v
```

Este esquema define la estructura de datos para actualizar un animal existente, con validaciones similares a `AnimalCreate`, pero permitiendo que los campos sean opcionales.

### 📋 AnimalResponse

```python
class AnimalResponse(BaseModel):
    """Schema for the response of an animal registration."""

    id: int
    """The ID of the animal"""
    nombre: str
    """The name of the animal"""
    raza: str
    """The breed of the animal"""
    edad: int
    """The age of the animal"""
    created_at: datetime
    """The timestamp when the animal was registered"""

    class Config:
        orm_mode = True
        from_attributes = True
```

Este esquema define la estructura de datos para las respuestas de la API, incluyendo todos los campos del modelo `Register`.
