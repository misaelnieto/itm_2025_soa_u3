s

Documentación del Frontend en React

Estructura del Proyecto

/imayo
├── /src
│   ├── /components
│   │   ├── EventForm.js
│   │   ├── EventsList.js
│   ├── /services
│   │   ├── api.js
│   ├── App.js
│   ├── index.js

Descripción General

Este proyecto es un frontend en React para la gestión de eventos. Cuenta con un formulario para agregar o editar eventos y una lista para visualizar, editar y eliminar eventos.

Componentes

1. EventForm.js

Ubicación: src/components/EventForm.js

Este componente maneja la creación y edición de eventos. Incluye validaciones para evitar números en los campos de nombre y descripción.

Props:

existingEvent: Objeto con la información de un evento para editar (opcional).

onSuccess: Función a ejecutar después de agregar o actualizar un evento.

Funciones principales:

validateInput(): Valida que los campos de nombre y descripción no contengan números.

handleSubmit(): Maneja el envío del formulario para crear o actualizar un evento.

Ejemplo de Uso:

<EventForm existingEvent={event} onSuccess={fetchEvents} />

2. EventsList.js

Ubicación: src/components/EventsList.js

Este componente muestra la lista de eventos y permite editarlos o eliminarlos. También incluye el formulario EventForm.js para la creación y edición de eventos.

Estados:

events: Lista de eventos obtenidos de la API.

editingEvent: Evento seleccionado para edición.

Funciones principales:

fetchEvents(): Obtiene los eventos desde la API.

handleDelete(id): Elimina un evento por su ID tras confirmación del usuario.

Ejemplo de Uso:

<EventsList />

Servicios

api.js

Ubicación: src/services/api.js

Este archivo maneja las peticiones HTTP a la API para la gestión de eventos.

Funciones principales:

createEvent(data): Crea un nuevo evento.

getEvents(): Obtiene la lista de eventos.

updateEvent(id, data): Actualiza un evento por su ID.

deleteEvent(id): Elimina un evento por su ID.

Aplicación Principal

App.js

Ubicación: src/App.js

Este archivo contiene la estructura principal de la aplicación e integra los componentes EventsList.js.

Ejemplo de Uso:

import React from 'react';
import EventsList from './components/EventsList';

function App() {
  return (
    <div className="container">
      <h1>Gestión de Eventos</h1>
      <EventsList />
    </div>
  );
}

export default App;

Instalación y Ejecución

Clona el repositorio:

git clone https://github.com/tu-repo.git
cd imayo

Instala las dependencias:

npm install

Ejecuta el proyecto:

npm start

Esto iniciará el servidor en http://localhost:3000/.