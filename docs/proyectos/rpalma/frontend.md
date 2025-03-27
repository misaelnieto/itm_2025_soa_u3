# Documentación del Frontend

## Archivos

### `contactos.html`

Este archivo contiene la estructura principal de la interfaz de usuario para la agenda de contactos. Incluye:

- **Encabezado HTML**: Define los metadatos, enlaces a hojas de estilo y scripts necesarios.
- **Botón "Cargar Datos"**: Permite cargar los contactos desde la base de datos.
- **Buscador**: Un campo de entrada para filtrar contactos por nombre.
- **Botón "Add New"**: Permite agregar un nuevo contacto.
- **Tabla**: Muestra los contactos con columnas para ID, nombre, teléfono, correo y acciones (editar/eliminar).

---

### `scripts.js`

Este archivo contiene la lógica de la aplicación para interactuar con la API y manejar eventos en la interfaz. A continuación, se explican las funciones principales:

#### **1. `mostrarMensaje(mensaje, tipo)`**
Muestra mensajes de alerta en la interfaz (éxito, advertencia o error).
- **Parámetros**:

  - `mensaje`: Texto del mensaje a mostrar.
  - `tipo`: Clase CSS para el tipo de mensaje (`alert-success`, `alert-danger`, etc.).
- **Uso**: Se utiliza para notificar al usuario sobre el resultado de las operaciones (por ejemplo, éxito al cargar datos o error al eliminar un contacto).

#### **2. `cargarDatos()`**
Carga la lista de contactos desde la API y los muestra en la tabla.
- **Flujo**:

  1. Realiza una solicitud `GET` al endpoint `/agenda`.
  2. Si hay contactos, los agrega a la tabla.
  3. Si no hay contactos, muestra un mensaje de advertencia.
  4. Habilita el campo de "Filtrar por nombre" y el boton de "Add new".
- **Uso**: Se ejecuta al cargar la página o al realizar cambios en los contactos.

#### **3. `buscarContacto()`**
Busca un contacto por nombre en la API.
- **Flujo**:

  1. Obtiene el nombre ingresado en el campo de búsqueda.
  2. Realiza una solicitud `GET` al endpoint `/search/{nombre}`.
  3. Muestra los resultados en la tabla o un mensaje si no se encuentran coincidencias.
- **Uso**: Se activa al hacer clic en el botón de búsqueda.

#### **4. Evento: `click` en `.btn_new`**
Permite agregar una fila temporal en la tabla para crear un nuevo contacto.
- **Flujo**:
  1. Elimina cualquier fila temporal existente para evitar duplicados.
  2. Agrega una nueva fila temporal con campos de entrada (`<input>`) para capturar los datos del nuevo contacto.
  3. Habilita el botón ".add (Guardar)" en la fila temporal.
- **Uso**: Se activa al hacer clic en el botón "Add New".

#### **5. Evento: `click` en `.add`**
Agrega un nuevo contacto a través de un formulario temporal.
- **Flujo**:

  1. Obtiene los valores ingresados en los campos de la fila temporal.
  2. Valida que los campos requeridos (nombre y teléfono) no estén vacíos.
  3. Realiza una solicitud `POST` al endpoint `/create`.
  4. Si la operación es exitosa, recarga los datos.
- **Uso**: Se activa al hacer clic en el botón "Guardar" de una fila temporal.

#### **6. Evento: `click` en `.edit`**
Habilita la edición de un contacto existente.
- **Flujo**:

  1. Convierte las celdas de la fila seleccionada en campos de entrada (`<input>`).
  2. Alterna los botones de acción para mostrar "Guardar Cambios".
- **Uso**: Se activa al hacer clic en el botón "Editar".

#### **7. Evento: `click` en `.save`**
Guarda los cambios realizados en un contacto editado (Guardar cambios).
- **Flujo**:

  1. Obtiene los valores ingresados en los campos de la fila.
  2. Valida que los campos requeridos (nombre y teléfono) no estén vacíos.
  3. Realiza una solicitud `PUT` al endpoint `/edit/{id}`.
  4. Si la operación es exitosa, recarga los datos.
- **Uso**: Se activa al hacer clic en el botón "Guardar Cambios".

#### **8. Evento: `click` en `.delete`**
Elimina un contacto de la base de datos.
- **Flujo**:
  1. Solicita confirmación al usuario antes de eliminar.
  2. Realiza una solicitud `DELETE` al endpoint `/delete/{id}`.
  3. Si la operación es exitosa, recarga los datos.
- **Uso**: Se activa al hacer clic en el botón "Eliminar".

---

### `styles.css`

Este archivo contiene los estilos personalizados para la interfaz de usuario. Principales características:

- **Vista general de la página**: Define los colores y fuentes de la página en general.
- **Estilo de la Tabla**: Define bordes, colores y espaciado para las filas y columnas.
- **Botones**: Personaliza los botones de acción como "Add New", "Cargar Datos" y "Buscar".
- **Mensajes de Alerta**: Estiliza los mensajes de éxito, advertencia y error.

---

## Dependencias

- **Bootstrap**: Para estilos y componentes responsivos.
- **jQuery**: Para manipulación del DOM y solicitudes AJAX.
- **Font Awesome y Material Icons**: Para iconos en la interfaz.

---

## Notas

- Asegúrate de que la API esté activa en `http://127.0.0.1:8000/api/v1/rpalma/contactos`.
- Los tooltips se reactivan dinámicamente después de cada acción para mantener la funcionalidad.
- Se hace un servidor HTTP en Python para mostrar este HTML en `http://127.0.0.1:3000/contactos` con el comando:
  ```bash
  cd c:/[ubicacion/del/html] 
  python -m http.server 3000 --bind 127.0.0.1
  ```
- Se tiene que agregar lo siguiente en `main.py` para que no haya problemas al consumir la API desde un navegador web:
  ```python
  from fastapi import FastAPI
  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],  # Evita usar "*"
      allow_credentials=True,
      allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
      allow_headers=["*"],  # Permite todos los encabezados.
  )
  ```