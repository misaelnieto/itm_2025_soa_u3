import React, { useState, useEffect } from 'react';
import { createEvent, updateEvent } from "../services/api";


/* Crear un nuevo componente llamado EventForm.js en la carpeta src/components. 
Este componente será un formulario para agregar o editar eventos.*/

const EventForm = ({ existingEvent, onSuccess }) => {
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [fecha, setFecha] = useState('');
  const [error, setError] = useState('');
/* Aqui se valida si existe los  */
  useEffect(() => {
    if (existingEvent) {
      setNombre(existingEvent.nombre);
      setDescripcion(existingEvent.descripcion);
      setFecha(existingEvent.fecha);
    }
  }, [existingEvent]);

  // Función para validar que no haya números en el nombre y la descripción
  const validateInput = () => {
    const regex = /\d/; // Expresión regular para detectar números
    if (regex.test(nombre)) {
      setError("El nombre no puede contener números.");
      return false;
    }
    if (regex.test(descripcion)) {
      setError("La descripción no puede contener números.");
      return false;
    }
    setError('');
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validar los campos antes de enviar el formulario
    if (!validateInput()) {
      return;
    }

    const eventData = {
      nombre,
      descripcion,
      fecha,
    };

    if (existingEvent) {
      await updateEvent(existingEvent.id, eventData);
    } else {
      await createEvent(eventData);
    }

    onSuccess();
    setNombre('');
    setDescripcion('');
    setFecha('');
  };

  return (
    <form onSubmit={handleSubmit} className="bg-light p-4 rounded shadow">
      <h3>{existingEvent ? 'Editar Evento' : 'Agregar Evento'}</h3>
      <div className="form-group">
        <label>Nombre:</label>
        <input
          type="text"
          className="form-control"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label>Descripción:</label>
        <textarea
          className="form-control"
          value={descripcion}
          onChange={(e) => setDescripcion(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label>Fecha:</label>
        <input
          type="datetime-local"
          className="form-control"
          value={fecha}
          onChange={(e) => setFecha(e.target.value)}
          required
        />
      </div>
      {error && <p className="text-danger">{error}</p>}
      <button type="submit" className="btn btn-primary btn-block">
        {existingEvent ? 'Actualizar' : 'Agregar'}
      </button>
    </form>
  );
};

export default EventForm;
