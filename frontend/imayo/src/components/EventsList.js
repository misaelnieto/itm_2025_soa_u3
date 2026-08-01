import React, { useEffect, useState } from "react";
import { getEvents, deleteEvent } from "../services/api";
import EventForm from "./EventForm";

const EventsList = () => {
  const [events, setEvents] = useState([]);
  const [editingEvent, setEditingEvent] = useState(null);

  const fetchEvents = async () => {
    try {
      const data = await getEvents();
      setEvents(data);
    } catch (error) {
      console.error("Error al cargar los eventos:", error);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm("¿Estás seguro de que deseas eliminar este evento?")) {
      await deleteEvent(id);
      fetchEvents();
    }
  };

  return (
    <div className="row">
      <div className="col-md-8">
        <h2 className="mb-4">Lista de Eventos</h2>
        <ul className="list-group">
          {events.map(event => (
            <li key={event.id} className="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <h4>{event.nombre}</h4>
                <p>{event.descripcion}</p>
                <p>{new Date(event.fecha).toLocaleString()}</p>
              </div>
              <div>
                <button
                  className="btn btn-warning btn-sm"
                  onClick={() => setEditingEvent(event)}
                >
                  Editar
                </button>
                <button
                  className="btn btn-danger btn-sm ml-2"
                  onClick={() => handleDelete(event.id)}
                >
                  Eliminar
                </button>
              </div>
            </li>
          ))}
        </ul>
      </div>
      <div className="col-md-4">
        <EventForm existingEvent={editingEvent} onSuccess={fetchEvents} />
      </div>
    </div>
  );
};

export default EventsList;