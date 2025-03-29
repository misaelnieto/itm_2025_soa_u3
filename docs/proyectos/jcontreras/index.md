# Proyecto Ventas


!!! tip "Descripción General"
    El proyecto **Ventas** es un ejemplo práctico de cómo crear un API REST utilizando Python y FastAPI. Incluye un backend, un frontend y pruebas automatizadas.

---

## Descripción general del funcionamiento del backend y el frontend

El backend está construido con [FastAPI](https://fastapi.tiangolo.com/). Los archivos de implementación se encuentran en la ruta `/app/proyectos/jcontreras`. Ahi se definen tres operaciones principales:

- Descarga de transacciones

El frontend está construido con la ayuda del Framework [NextJS](https://nextjs.org/) para la construir la interfaz grafica de usuario y se usa la interfaz nativa `fetch` de JavaScript para comunicarse con la base de datos. El frontend se conecta al backend mediante la url `http://127.0.0.1:8000/api/v1/jcontreras/ventas`.

### Carga inicial de datos


Para iniciar el Frontend primero debemos de ir al directorio `./frontend/jcontreras` y ejecutar `npm install && npm run dev` y el frontend se iniciara en `http://localhost:3000`

A continuación se muestra un diagrama de secuencia que muestra la comunicación inicial entre el frontend y el backend, justo después de que el usuario accedió al frontend.

```mermaid
sequenceDiagram
    participant Usuario
    participant Frontend
    participant Backend


    Usuario-->>Frontend: Arranca frontend de ventas
    Note over Usuario, Backend: Carga inicial de datos
    rect rgb(191, 123, 155)
        activate Frontend
            Frontend->>Backend: GET /api/v1/jcontreras/ventas/
            activate Backend
            Backend-->>Frontend: Retorna la lista de ventas
            deactivate Backend
            Note right of Frontend: Muestra lista de ventas en tabla
            Note right of Frontend: 
            Frontend-->>Usuario: Lista de transacciones
        deactivate Frontend
    end
```

### Creación de ventas

Una vez que el usuario arranco el frontend y los datos iniciales han sido cargados, el usuario puede dar de alta un ventas mediante el boton *Crear ventas*. Cuando el usuario pica el boton se le muestra el siguiente formulario.


![Captura de pantalla del formulario de ventas](image.png)

El formulario tiene validaciones basicas como que el ISBN debe tener entre 10 y 13 caracteres, el titulo y autor no puede estar vacio ni solo espacios, tambien el boton *Guardar* estara deshabilitado hasta que todo este escrito de manera correcta.


Si el usuario introdujo algun dato que no cumpla con los requerimientos se lanzara un mensaje de error para que se validen los campos


![Captura de pantalla del frontend con mensaje de error](image-1.png)

### Creacion de ventas

```mermaid
sequenceDiagram
    participant Usuario
    participant Frontend
    participant Backend

    Note over Usuario, Backend: Proceso de alta
    rect rgb(91, 23, 155)
    Usuario->>Frontend: Se crea un ventas
    Frontend->>Backend: POST /api/v1/jcontreras/ventas/ `{cliente: "Javier", Producto: "PC GAMER", Cantidad: "1", Precio: "5000"}`
    Backend-->>Frontend: ventas Creado
    Frontend->>Backend: GET /api/v1/jcontreras/ventas/
    Backend-->>Frontend: Retorna la lista de ventas
    Note right of Frontend: Actualiza la lista de ventas
    end
```

Finalmente, la aplicacion de frontend de ventas luce asi despues de varios registros.


![Captura de pantalla despues de varias altas](image-2.png)

### Actualizacion de ventas

Para poder actualizar ventas se hace click en el boton de editar y nos despliegara la siguiente ventana

![Modal de modificar ventas](image-3.png)

```mermaid
sequenceDiagram
    participant Usuario
    participant Frontend
    participant Backend

    Note over Usuario, Backend: Proceso de actualizacion
    rect rgb(91, 23, 55)
    Frontend-->>Usuario: Lista de ventas
    Usuario->>Frontend: Realiza una actualizacion al ventas PC GAMER
    Frontend->>Backend: PUT /api/v1/jcontreras/ventas/2
    Note right of Frontend: {cliente: "Javier", Producto: "MONITOR", Cantidad: "1", Precio: "5000"}
    Backend-->>Frontend: Transacción exitosa
    Frontend->>Backend: GET /api/v1/jcontreras/ventas
    Backend-->>Frontend: Retorna la lista de ventas
    Note right of Frontend: Actualiza la lista de ventas
    end
```


---

## Backend - Detalle

El código fuente del backend se encuentra en el módulo `app/proyectos/jcontreras`. Está desarrollado utilizando FastAPI y expone tres rutas:

- **`GET /ventas`**: Obtiene el estado actual de la libreria. [Link a la funcion](backend.md#app.proyectos.jcontreras.routes.get_ventas)
- **`POST /ventas`**: Permite dar de alta un ventas en la libreria. [Link a la funcion](backend.md#app.proyectos.jcontreras.routes.create_ventas)
- **`PUT /ventas/{ventas_id}`**: Permite actualizar un ventas existente. [Link a la funcion](backend.md#app.proyectos.jcontreras.routes.update_ventas)
- **`DELETE /ventas/{ventas_id}`**: Permite borrar un ventas existente. [Link a la funcion](backend.md#app.proyectos.jcontreras.routes.delete_ventas)

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

Las pruebas automatizadas del backend se encuentran en el directorio `/tests/jcontreras`. Estas pruebas verifican el correcto funcionamiento de las rutas y la lógica de negocio.

[Documentación de funciones de prueba](tests.md){ .md-button .md-button--primary}

### Cómo ejecutar las pruebas
Para ejecutar las pruebas, utiliza el siguiente comando:

```bash
uv run pytest
```

---

## Frontend

El código fuente del frontend se encuentra en el archivo `/frontend/jcontreras`. Este módulo interactúa con el backend para mostrar el estado de la libreria y permitir operaciones como alta y baja.

[Documentación de Funciones del frontend](frontend.md){ .md-button .md-button--primary}


### Cómo arrancar el frontend

Primero arranca el backend, luego abre otra terminal y utiliza el siguiente comando:

```bash
python -m http.server 3000 --bind 127.0.0.1
```
