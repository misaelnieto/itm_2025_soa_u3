'use client';
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function CreateBook() {
  // Estados para almacenar los valores del formulario
  const [nombre, setNombre] = useState(""); // Cambiado de isbn a nombre
  const [tipo, setTipo] = useState(""); // Cambiado de titulo a tipo
  const [precio, setPrecio] = useState(""); // Cambiado de autor a precio
  const [errors, setErrors] = useState({}); // Estado para manejar los errores de validación
  const router = useRouter(); // Hook para manejar la navegación en Next.js

  // Función para validar los campos del formulario
  const validateFields = () => {
    let newErrors = {};
    if (!nombre.trim()) {
      newErrors.nombre = "El nombre no puede estar vacío";
    }
    if (!tipo.trim()) {
      newErrors.tipo = "El tipo no puede estar vacío";
    }
    if (!precio || isNaN(precio) || precio <= 0) {
      newErrors.precio = "El precio debe ser un número mayor a 0";
    }
    setErrors(newErrors); // Guardamos los errores en el estado
    return Object.keys(newErrors).length === 0; // Retorna true si no hay errores
  };

  // Manejo del envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault(); // Evita que el formulario recargue la página
    if (!validateFields()) { // Si la validación falla, no se envía la solicitud
    
    try {
      // Enviamos la solicitud a la API para crear un nuevo libro
      const response = await fetch("http://127.0.0.1:8000/api/v1/dramos/productos/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nombre, tipo, precio }),
      });
      
      if (response.ok) {
        router.push("/"); // Redirige al usuario a la página principal si la solicitud es exitosa
      } else {
        console.error("Failed to create product");
      }
    } catch (error) {
      console.error("Error:", error); // Manejo de errores en caso de fallo en la solicitud
    }
  }
};

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1 className="mt-8">Añade tu producto</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        {/* Campo de entrada para el nombre */}
        <input
          type="text"
          placeholder="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          className="p-2 border border-gray-300 rounded"
          required
        />
        {errors.nombre && <p className="text-red-500 text-sm">{errors.nombre}</p>}

        {/* Campo de entrada para el tipo */}
        <input
          type="text"
          placeholder="Tipo"
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
          className="p-2 border border-gray-300 rounded"
          required
        />
        {errors.tipo && <p className="text-red-500 text-sm">{errors.tipo}</p>}

        {/* Campo de entrada para el precio */}
        <input
          type="number"
          placeholder="Precio"
          value={precio}
          onChange={(e) => setPrecio(e.target.value)}
          className="p-2 border border-gray-300 rounded"
          required
        />
        {errors.precio && <p className="text-red-500 text-sm">{errors.precio}</p>}

        {/* Botón para enviar el formulario */}
        <button
          type="submit"
          className="p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Guardar
        </button>
      </form>
    </div>
  );
}