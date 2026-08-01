import { useState, useEffect } from "react";
import "../styles/global.css";

// Componente principal para el CRUD de animales
export default function AnimalesCrud({ apiUrl }) {
  const [animales, setAnimales] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({ nombre: "", raza: "", edad: "" });
  const [editingId, setEditingId] = useState(null);
  const [alert, setAlert] = useState(null);

  const baseUrl = `${apiUrl}/animales`;

  // Cargar animales al iniciar
  useEffect(() => {
    fetchAnimales();
  }, []);

  // Mostrar alerta temporal
  const showAlert = (message, type = "success") => {
    setAlert({ message, type });
    setTimeout(() => setAlert(null), 3000);
  };

  // Obtener todos los animales
  const fetchAnimales = async () => {
    setLoading(true);
    try {
      const response = await fetch(baseUrl);
      if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
      const data = await response.json();
      setAnimales(data);
    } catch (error) {
      console.error("Error al obtener animales:", error);
      showAlert(`Error al cargar los animales: ${error.message}`, "error");
    } finally {
      setLoading(false);
    }
  };

  // Manejar cambios en el formulario
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === "edad" ? parseInt(value) || "" : value,
    });
  };

  // Agregar o actualizar animal
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.nombre || !formData.raza || !formData.edad) {
      showAlert("Por favor complete todos los campos correctamente", "warning");
      return;
    }

    try {
      const isEditing = editingId !== null;
      const url = isEditing ? `${baseUrl}/${editingId}` : baseUrl;
      const method = isEditing ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Error HTTP: ${response.status}`);
      }

      await fetchAnimales();
      showAlert(
        `Animal ${isEditing ? "actualizado" : "agregado"} correctamente`
      );
      setFormData({ nombre: "", raza: "", edad: "" });
      setEditingId(null);
    } catch (error) {
      console.error(
        `Error al ${editingId ? "actualizar" : "agregar"} animal:`,
        error
      );
      showAlert(`Error: ${error.message}`, "error");
    }
  };

  // Preparar edición
  const handleEdit = (animal) => {
    setFormData({
      nombre: animal.nombre,
      raza: animal.raza,
      edad: animal.edad,
    });
    setEditingId(animal.id);
    // Hacer scroll al formulario
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Eliminar animal
  const handleDelete = async (id) => {
    if (!confirm("¿Está seguro de que desea eliminar este animal?")) return;

    try {
      const response = await fetch(`${baseUrl}/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);

      await fetchAnimales();
      showAlert("Animal eliminado correctamente");
    } catch (error) {
      console.error("Error al eliminar animal:", error);
      showAlert(`Error al eliminar: ${error.message}`, "error");
    }
  };

  // Formatear fecha
  const formatDate = (dateStr) => {
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString();
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="space-y-8 m-auto">
      {/* Formulario */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-bold mb-4 text-neutral-900 ">
          {editingId ? "Editar Animal" : "Agregar Animal"}
        </h2>
        <form
          onSubmit={handleSubmit}
          className="grid grid-cols-1 md:grid-cols-3 gap-4"
        >
          <div>
            <label className="block text-gray-700 mb-2">Nombre</label>
            <input
              type="text"
              name="nombre"
              value={formData.nombre}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border rounded-lg"
              required
            />
          </div>
          <div>
            <label className="block text-gray-700 mb-2">Raza</label>
            <input
              type="text"
              name="raza"
              value={formData.raza}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border rounded-lg"
              required
            />
          </div>
          <div>
            <label className="block text-gray-700 mb-2">Edad</label>
            <input
              type="number"
              name="edad"
              value={formData.edad}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border rounded-lg"
              min="0"
              required
            />
          </div>
          <div className="md:col-span-3 flex justify-end gap-2">
            {editingId && (
              <button
                type="button"
                onClick={() => {
                  setFormData({ nombre: "", raza: "", edad: "" });
                  setEditingId(null);
                }}
                className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:cursor-pointer"
              >
                Cancelar
              </button>
            )}
            <button
              type="submit"
              className={`px-4 py-2 ${
                editingId ? "bg-yellow-600" : "bg-neutral-900"
              } text-white rounded-lg hover:cursor-pointer`}
            >
              {editingId ? "Actualizar" : "Agregar"}
            </button>
          </div>
        </form>
      </div>

      {/* Tabla de animales */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="bg-neutral-900 text-white px-6 py-4 flex justify-between items-center">
          <h2 className="text-xl font-bold">Lista de Animales</h2>
          <button
            onClick={fetchAnimales}
            className="bg-white text-neutral-900 px-3 py-1 rounded"
          >
            Refrescar
          </button>
        </div>
        <div className="p-4">
          {loading ? (
            <div className="text-center py-4">Cargando...</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="py-2 px-3 text-left">ID</th>
                    <th className="py-2 px-3 text-left">Nombre</th>
                    <th className="py-2 px-3 text-left">Raza</th>
                    <th className="py-2 px-3 text-left">Edad</th>
                    <th className="py-2 px-3 text-left">Fecha</th>
                    <th className="py-2 px-3 text-left">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {animales.length === 0 ? (
                    <tr>
                      <td
                        colSpan="6"
                        className="text-center py-4 text-gray-500"
                      >
                        No hay animales registrados
                      </td>
                    </tr>
                  ) : (
                    animales.map((animal) => (
                      <tr key={animal.id} className="border-b hover:bg-gray-50">
                        <td className="py-2 px-3">{animal.id}</td>
                        <td className="py-2 px-3">{animal.nombre}</td>
                        <td className="py-2 px-3">{animal.raza}</td>
                        <td className="py-2 px-3">{animal.edad}</td>
                        <td className="py-2 px-3">
                          {formatDate(animal.created_at)}
                        </td>
                        <td className="py-2 px-3 space-x-1">
                          <button
                            onClick={() => handleEdit(animal)}
                            className="px-2 py-1 bg-yellow-500 text-white rounded hover:cursor-pointer"
                          >
                            Editar
                          </button>
                          <button
                            onClick={() => handleDelete(animal.id)}
                            className="px-2 py-1 bg-red-500 text-white rounded hover:cursor-pointer"
                          >
                            Eliminar
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Alerta simple */}
      {alert && (
        <div
          className={`fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg ${
            alert.type === "error"
              ? "bg-red-500"
              : alert.type === "warning"
              ? "bg-yellow-500"
              : "bg-green-500"
          } text-white`}
        >
          {alert.message}
        </div>
      )}
    </div>
  );
}
