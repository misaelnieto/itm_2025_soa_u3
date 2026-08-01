'use client';
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function CreateBook() {
  // Estados para almacenar los valores del formulario
  const [isbn, setIsbn] = useState("");
  const [titulo, setTitulo] = useState("");
  const [autor, setAutor] = useState("");
  const [errors, setErrors] = useState({}); // Estado para manejar los errores de validación
  const router = useRouter(); // Hook para manejar la navegación en Next.js

  // Función para validar los campos del formulario
  const validateFields = () => {
    let newErrors = {};
    if (!/^(\\d{10}|\\d{13})$/.test(isbn)) {
      newErrors.isbn = "El ISBN debe tener 10 o 13 dígitos numéricos";
    }
    if (!titulo.trim()) {
      newErrors.titulo = "El título no puede estar vacío";
    }
    if (!autor.trim()) {
      newErrors.autor = "El autor no puede estar vacío";
    }
    setErrors(newErrors); // Guardamos los errores en el estado
    return Object.keys(newErrors).length === 0; // Retorna true si no hay errores
  };

  // Manejo del envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault(); // Evita que el formulario recargue la página
    if (!validateFields()) return; // Si la validación falla, no se envía la solicitud
    
    try {
      // Enviamos la solicitud a la API para crear un nuevo libro
      const response = await fetch("http://127.0.0.1:8000/api/v1/jparedes/libros/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ isbn, titulo, autor }),
      });
      
      if (response.ok) {
        router.push("/"); // Redirige al usuario a la página principal si la solicitud es exitosa
      } else {
        console.error("Failed to create book");
      }
    } catch (error) {
      console.error("Error:", error); // Manejo de errores en caso de fallo en la solicitud
    }
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1>Añade tu libro</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        {/* Campo de entrada para el ISBN */}
        <input
          type="text"
          placeholder="ISBN"
          value={isbn}
          onChange={(e) => setIsbn(e.target.value)}
          className="p-2 border border-gray-300 rounded"
          required
        />
        {errors.isbn && <p className="text-red-500 text-sm">{errors.isbn}</p>}

        {/* Campo de entrada para el título */}
        <input
          type="text"
          placeholder="Título"
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
          className="p-2 border border-gray-300 rounded"
          required
        />
        {errors.titulo && <p className="text-red-500 text-sm">{errors.titulo}</p>}

        {/* Campo de entrada para el autor */}
        <input
          type="text"
          placeholder="Autor"
          value={autor}
          onChange={(e) => setAutor(e.target.value)}
          className="p-2 border border-gray-300 rounded"
          required
        />
        {errors.autor && <p className="text-red-500 text-sm">{errors.autor}</p>}

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
