// src/services/api.js
import axios from 'axios';

const API_BASE_URL = "http://localhost:8000/api/v1/imayo/eventos";

export const getEvents = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/`, {
      headers: {
        Authorization: `Bearer YOUR_ACCESS_TOKEN`, // Reemplaza con tu token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error al obtener los eventos:", error);
    throw error;
  }
};

export const createEvent = async (eventData) => {
try {
    const response = await axios.post(`${API_BASE_URL}/`, eventData);
    return response.data;
} catch (error) {
    console.error("Error al crear el evento:", error);
    throw error;
}
};

export const updateEvent = async (id, eventData) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/${id}/`, eventData);
      return response.data;
    } catch (error) {
      console.error("Error al actualizar el evento:", error);
      throw error;
    }
  };
  
  export const deleteEvent = async (id) => {
    try {
      await axios.delete(`${API_BASE_URL}/${id}/`);
    } catch (error) {
      console.error("Error al eliminar el evento:", error);
      throw error;
    }
  };
  
