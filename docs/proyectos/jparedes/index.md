# Proyecto Libreria


!!! tip "Descripción General"
    El proyecto **Libreria** es un ejemplo práctico de cómo crear un API REST utilizando Python y FastAPI. Incluye un backend, un frontend y pruebas automatizadas.

---

## Descripción general del funcionamiento del backend y el frontend

El backend está construido con [FastAPI](https://fastapi.tiangolo.com/). Los archivos de implementación se encuentran en la ruta `/app/proyectos/jparedes`. Ahi se definen tres operaciones principales:

- Descarga de transacciones

El frontend está construido con la ayuda del Framework [NextJS](https://nextjs.org/) para la construir la interfaz grafica de usuario y se usa la interfaz nativa `fetch` de JavaScript para comunicarse con la base de datos. El frontend se conecta al backend mediante la url `http://127.0.0.1:8000/api/v1/jparedes/libros`.

### Carga inicial de datos


Para iniciar el Frontend primero debemos de ir al directorio `./frontend/jparedes` y ejecutar `npm install && npm run dev` y el frontend se iniciara en `http://localhost:3000`

A continuación se muestra un diagrama de secuencia que muestra la comunicación inicial entre el frontend y el backend, justo después de que el usuario accedió al frontend.

```mermaid
sequenceDiagram
    participant Usuario
    participant Frontend
    participant Backend


    Usuario-->>Frontend: Arranca frontend de Libros
    Note over Usuario, Backend: Carga inicial de datos
    rect rgb(191, 123, 155)
        activate Frontend
            Frontend->>Backend: GET /api/v1/jparedes/libros/
            activate Backend
            Backend-->>Frontend: Retorna la lista de libros
            deactivate Backend
            Note right of Frontend: Muestra lista de libros en tabla
            Note right of Frontend: 
            Frontend-->>Usuario: Lista de transacciones
        deactivate Frontend
    end
```

### Creación de Libros

Una vez que el usuario arranco el frontend y los datos iniciales han sido cargados, el usuario puede dar de alta un libro mediante el boton *Crear Libro*. Cuando el usuario pica el boton se le muestra el siguiente formulario.


![Captura de pantalla del formulario de libros](image.png)

El formulario tiene validaciones basicas como que el ISBN debe tener entre 10 y 13 caracteres, el titulo y autor no puede estar vacio ni solo espacios, tambien el boton *Guardar* estara deshabilitado hasta que todo este escrito de manera correcta.


Si el usuario introdujo algun dato que no cumpla con los requerimientos se lanzara un mensaje de error para que se validen los campos


![Captura de pantalla del frontend con mensaje de error](image-1.png)

### Creacion de libros

```mermaid
sequenceDiagram
    participant Usuario
    participant Frontend
    participant Backend

    Note over Usuario, Backend: Proceso de alta
    rect rgb(91, 23, 155)
    Usuario->>Frontend: Se crea un libro
    Frontend->>Backend: POST /api/v1/jparedes/libros/ `{isbn: 1234567890, titulo: "Harry Potter", autor: "JK Rowling"}`
    Backend-->>Frontend: Libro Creado
    Frontend->>Backend: GET /api/v1/jparedes/libros/
    Backend-->>Frontend: Retorna la lista de libros
    Note right of Frontend: Actualiza la lista de libros
    end
```

Finalmente, la aplicacion de frontend de libros luce asi despues de varios depositos.


![Captura de pantalla despues de varias altas](image-2.png)

### Actualizacion de libros

Para poder actualizar libro se hace click en el boton de editar y nos despliegara la siguiente ventana

![Modal de modificar libro](image-3.png)

```mermaid
sequenceDiagram
    participant Usuario
    participant Frontend
    participant Backend

    Note over Usuario, Backend: Proceso de actualizacion
    rect rgb(91, 23, 55)
    Frontend-->>Usuario: Lista de libros
    Usuario->>Frontend: Realiza una actualizacion al libro harry potter
    Frontend->>Backend: PUT /api/v1/jparedes/libros/2
    Note right of Frontend: {"id": 2, "titulo": "Harry Potter", autor: "Jk rowling jr"}
    Backend-->>Frontend: Transacción exitosa
    Frontend->>Backend: GET /api/v1/jparedes/libros
    Backend-->>Frontend: Retorna la lista de libros
    Note right of Frontend: Actualiza la lista de libros
    end
```


---

## Backend - Detalle

El código fuente del backend se encuentra en el módulo `app/proyectos/jparedes`. Está desarrollado utilizando FastAPI y expone tres rutas:

- **`GET /libros`**: Obtiene el estado actual de la libreria. [Link a la funcion](backend.md#app.proyectos.jparedes.routes.get_libros)
- **`POST /libros`**: Permite dar de alta un libro en la libreria. [Link a la funcion](backend.md#app.proyectos.jparedes.routes.create_libro)
- **`PUT /libros/{libro_id}`**: Permite actualizar un libro existente. [Link a la funcion](backend.md#app.proyectos.jparedes.routes.update_libro)
- **`DELETE /libros/{libro_id}`**: Permite borrar un libro existente. [Link a la funcion](backend.md#app.proyectos.jparedes.routes.delete_libro)

A continuacion se muestran los links a la documentación de cada submódulo.

[Documentación de rutas](autodocs.md#routes){ .md-button .md-button--primary}
[Documentación de modelos](autodocs.md#models){ .md-button .md-button--primary}
[Documentación de esquemas](autodocs.md#schemas){ .md-button .md-button--primary}


### Cómo arrancar el backend

Para iniciar el backend, utiliza el siguiente comando:

```bash
uv run fastapi run
```

---

## Pruebas del Backend

Las pruebas automatizadas del backend se encuentran en el directorio `/tests/jparedes`. Estas pruebas verifican el correcto funcionamiento de las rutas y la lógica de negocio.

[Documentación de funciones de prueba](tests.md){ .md-button .md-button--primary}

### Cómo ejecutar las pruebas
Para ejecutar las pruebas, utiliza el siguiente comando:

```bash
uv run pytest
```

---

## Frontend

El código fuente del frontend se encuentra en el archivo `/frontend/jparedes`. Este módulo interactúa con el backend para mostrar el estado de la libreria y permitir operaciones como alta y baja.

[Documentación de Funciones del frontend](frontend.md){ .md-button .md-button--primary}


### Cómo arrancar el frontend

Primero arranca el backend, luego abre otra terminal y utiliza el siguiente comando:

```bash
cd frontend/jparedes
npm install
npm run dev
```
