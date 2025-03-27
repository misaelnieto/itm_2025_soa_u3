# Routes de Backend

Este documento describe las rutas y funcionalidades de la API de Recetas en la aplicación "Receta". La API permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre las recetas almacenadas en la base de datos.

## `GET /recetas/todas`
- **Descripción**: Recupera la lista de todas las recetas almacenadas en la base de datos.
- **Función asociada**: `recipes_list`.
- **Retorno**: Una lista de objetos `Receta`.


## `GET /recetas/receta`
- **Descripción**: Recupera una receta específica por su ID.
- **Función asociada**: `get_receta`.
- **Parámetros**:
  - `receta_id` (int): El ID de la receta a recuperar.
- **Retorno**: Un objeto `Receta` si existe, o un error 404 si no se encuentra.


## `POST /recetas/alta`
- **Descripción**: Permite subir una nueva receta a la base de datos.
- **Función asociada**: `upload_receta`.
- **Cuerpo de la solicitud**: Un objeto JSON con los datos de la receta.
- **Retorno**: Un código de estado 201 si la receta se crea correctamente.


## Documentación autogenerada

[Documentación de rutas](backend.md#routes){ .md-button .md-button--primary}
</br>

---
# Model de Recetas 
Este documento describe los modelos de datos utilizados en la API de Recetas. Los modelos están definidos en el archivo `models.py` y representan las entidades principales de la base de datos.


## `Receta`
- **Descripción**: Representa una receta en la base de datos.
- **Tabla asociada**: `receta`.
- **Atributos**:
  - `id` (int): Identificador único de la receta. Es la clave primaria.
  - `nombre` (str): Nombre de la receta.
  - `descripcion` (str): Descripción de la receta.
  - `min_preparacion` (int): Tiempo de preparación en minutos.
  - `ingredientes` (str): Lista de ingredientes necesarios para la receta.
  - `metodo_preparacion` (str): Método de preparación de la receta.
  - `created_at` (datetime): Fecha y hora de creación de la receta. Se genera automáticamente en UTC.

## Documentación Autogenerada
[Documentación de modelos](backend.md#models){ .md-button .md-button--primary}

---
# Esquemas de Backend


Este documento describe los esquemas utilizados en la API de Recetas. Los esquemas están definidos en el archivo `schemas.py` y se utilizan para validar y estructurar las respuestas de la API.


# `RecipeResponse`
- **Descripción**: Representa la respuesta estándar de las operaciones realizadas en la API de Recetas.
- **Atributos**:
  - `result` (`RecipeResult`): Indica el resultado de la operación (éxito o error).


## `RecipeResult`
- **Descripción**: Enumera los posibles resultados de las operaciones realizadas en la API.
- **Valores**:
  - `successful`: La operación se realizó con éxito.
  - `failed`: La operación falló.
  - `non_existent`: El recurso solicitado no existe.

## Documentación Autogenerada
[Documentación de esquemas](backend.md#schemas){ .md-button .md-button--primary}

---

# Pruebas
Este documento describe las pruebas definidas en el archivo `test_rgarcia.py`. Estas pruebas verifican el correcto funcionamiento de las rutas de la API de Recetas, asegurando que las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) se realicen correctamente.

# `test_all_recipes`
- **Descripción**: Verifica que la API pueda devolver la lista de todas las recetas.
- **Pasos**:
  1. Realiza una solicitud `GET` a `/recetas/todas`.
  2. Verifica que el código de estado sea `200 OK`.
  3. Comprueba que la respuesta sea una lista de objetos `Receta`.


# `test_existent_singular_recipe`
- **Descripción**: Verifica que la API pueda devolver una receta específica por su ID.
- **Pasos**:
  1. Crea una receta con un ID específico mediante una solicitud `POST` a `/recetas/alta`.
  2. Realiza una solicitud `GET` a `/recetas/receta` con el ID de la receta.
  3. Verifica que el código de estado sea `200 OK`.
  4. Comprueba que la respuesta sea un objeto `Receta`.


# `test_non_existent_recipe`
- **Descripción**: Verifica que la API devuelva un error `404 Not Found` al intentar acceder a una receta inexistente.
- **Pasos**:
  1. Realiza una solicitud `GET` a `/recetas/receta` con un ID que no existe.
  2. Verifica que el código de estado sea `404 Not Found`.


# `test_update_existent_recipe`
- **Descripción**: Verifica que la API pueda actualizar una receta existente.
- **Pasos**:
  1. Crea una receta mediante una solicitud `POST` a `/recetas/alta`.
  2. Realiza una solicitud `PUT` a `/recetas/modificar` con los datos actualizados de la receta.
  3. Verifica que el código de estado sea `204 No Content`.
  4. Realiza una solicitud `GET` a `/recetas/receta` para verificar que los datos se hayan actualizado correctamente.


# `test_update_non_existent_recipe`
- **Descripción**: Verifica que la API devuelva un error `404 Not Found` al intentar actualizar una receta inexistente.
- **Pasos**:
  1. Realiza una solicitud `PUT` a `/recetas/modificar` con un ID que no existe.
  2. Verifica que el código de estado sea `404 Not Found`.
## Documentación Autogenerada
[Documentación de funciones de prueba](tests.md){ .md-button .md-button--primary}

---

# Frontend
Este documento describe la funcionalidad del front-end de la aplicación "Recetas". El front-end interactúa con la API de Recetas para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) y mostrar los datos de las recetas al usuario.

El front-end de la aplicación "Recetas" está desarrollado utilizando **PyQt**, un conjunto de herramientas para crear interfaces gráficas de usuario (GUIs) en Python. Este front-end interactúa con la API de Recetas para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) y mostrar los datos de las recetas al usuario de manera visual e interactiva.


## Tecnologías Utilizadas
#### **PyQt**:
   - Proporciona los componentes necesarios para construir la interfaz gráfica de usuario.
   - Incluye widgets como tablas, formularios, botones y cuadros de diálogo para interactuar con las recetas.

#### **Requests**:
   - Se utiliza para realizar solicitudes HTTP (`GET`, `POST`, `PUT`, `DELETE`) a los endpoints de la API de Recetas.
   - Procesa las respuestas de la API y actualiza los datos en la interfaz gráfica.

#### **JSON**:
   - Se utiliza para manejar los datos enviados y recibidos desde la API en formato JSON.

## Funcionalidades

### 1. **Lista de Recetas**
- **Descripción**: Muestra una lista de todas las recetas disponibles en la base de datos.
- **Interacción con la API**:
  - Realiza una solicitud `GET` a `/recetas/todas`.
- **Comportamiento**:
  - Si la solicitud es exitosa, muestra las recetas en una tabla o lista.
  - Si ocurre un error, muestra un mensaje de error al usuario.


### 2. **Detalle de una Receta**
- **Descripción**: Permite al usuario ver los detalles de una receta específica.
- **Interacción con la API**:
  - Realiza una solicitud `GET` a `/recetas/receta` con el parámetro `receta_id`.
- **Comportamiento**:
  - Si la receta existe, muestra sus detalles (nombre, descripción, ingredientes, método de preparación, etc.).
  - Si la receta no existe, muestra un mensaje de error.


### 3. **Crear una Nueva Receta**
- **Descripción**: Permite al usuario agregar una nueva receta a la base de datos.
- **Interacción con la API**:
  - Realiza una solicitud `POST` a `/recetas/alta` con los datos de la receta en formato JSON.
- **Comportamiento**:
  - Si la receta se crea correctamente, muestra un mensaje de éxito y actualiza la lista de recetas.
  - Si ocurre un error, muestra un mensaje de error.


### 4. **Actualizar una Receta**
- **Descripción**: Permite al usuario modificar los datos de una receta existente.
- **Interacción con la API**:
  - Realiza una solicitud `PUT` a `/recetas/modificar` con los datos actualizados de la receta en formato JSON.
- **Comportamiento**:
  - Si la receta se actualiza correctamente, muestra un mensaje de éxito y actualiza la lista de recetas.
  - Si la receta no existe, muestra un mensaje de error.


### 5. **Eliminar una Receta**
- **Descripción**: Permite al usuario eliminar una receta específica de la base de datos.
- **Interacción con la API**:
  - Realiza una solicitud `DELETE` a `/recetas/eliminar` con el parámetro `receta_id`.
- **Comportamiento**:
  - Si la receta se elimina correctamente, muestra un mensaje de éxito y actualiza la lista de recetas.
  - Si la receta no existe, muestra un mensaje de error.



## 1. **Lista de Recetas**
- **Descripción**: Muestra una lista de todas las recetas disponibles en la base de datos.
- **Interacción con la API**:
  - Realiza una solicitud `GET` a `/recetas/todas`.
- **Comportamiento**:
  - Si la solicitud es exitosa, muestra las recetas en una tabla o lista.
  - Si ocurre un error, muestra un mensaje de error al usuario.


## 2. **Detalle de una Receta**
- **Descripción**: Permite al usuario ver los detalles de una receta específica.
- **Interacción con la API**:
  - Realiza una solicitud `GET` a `/recetas/receta` con el parámetro `receta_id`.
- **Comportamiento**:
  - Si la receta existe, muestra sus detalles (nombre, descripción, ingredientes, método de preparación, etc.).
  - Si la receta no existe, muestra un mensaje de error.


## 3. **Crear una Nueva Receta**
- **Descripción**: Permite al usuario agregar una nueva receta a la base de datos.
- **Interacción con la API**:
  - Realiza una solicitud `POST` a `/recetas/alta` con los datos de la receta en formato JSON.
- **Comportamiento**:
  - Si la receta se crea correctamente, muestra un mensaje de éxito y actualiza la lista de recetas.
  - Si ocurre un error, muestra un mensaje de error.


## 4. **Actualizar una Receta**
- **Descripción**: Permite al usuario modificar los datos de una receta existente.
- **Interacción con la API**:
  - Realiza una solicitud `PUT` a `/recetas/modificar` con los datos actualizados de la receta en formato JSON.
- **Comportamiento**:
  - Si la receta se actualiza correctamente, muestra un mensaje de éxito y actualiza la lista de recetas.
  - Si la receta no existe, muestra un mensaje de error.


## 5. **Eliminar una Receta**
- **Descripción**: Permite al usuario eliminar una receta específica de la base de datos.
- **Interacción con la API**:
  - Realiza una solicitud `DELETE` a `/recetas/eliminar` con el parámetro `receta_id`.
- **Comportamiento**:
  - Si la receta se elimina correctamente, muestra un mensaje de éxito y actualiza la lista de recetas.
  - Si la receta no existe, muestra un mensaje de error.

## Documentación Autogenerada
[Documentación de Funciones del frontend](frontend.md){ .md-button .md-button--primary}