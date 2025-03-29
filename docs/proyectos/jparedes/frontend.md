# Frontend


## Creacion del frontend

Para la creacion del frontend se utilizo el framework de javascript [NextJS](https://nextjs.org/) con el siguiente comando

```bash
npm npx create-next-app@latest jparedes
```

Para ejecutarlo

```bash
npm install
npm run dev
```

Por defecto este framework tiene como pagina principal `/app/page.js`

```react
'use client';
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

/**
 * Componente principal que maneja la visualización, edición y eliminación de libros.
 */
export default function Home() {
  const [libros, setLibros] = useState([]); // Estado para almacenar la lista de libros
  const [isModalOpen, setIsModalOpen] = useState(false); // Estado para controlar la visibilidad del modal de edición
  const [selectedLibro, setSelectedLibro] = useState(null); // Estado para almacenar el libro seleccionado para edición
  const router = useRouter();

  /**
   * Obtiene la lista de libros desde la API al cargar el componente.
   */
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/jparedes/libros/')
      .then(response => response.json())
      .then(data => setLibros(data));
  }, []);

  /**
   * Maneja la apertura del modal de edición con los datos del libro seleccionado.
   * @param {Object} libro - Objeto que representa el libro seleccionado.
   */
  const handleEditClick = (libro) => {
    setSelectedLibro(libro);
    setIsModalOpen(true);
  };

  /**
   * Cierra el modal de edición y resetea el libro seleccionado.
   */
  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedLibro(null);
  };

  /**
   * Maneja el cambio en los campos del formulario de edición.
   * @param {Event} e - Evento de cambio en los inputs.
   */
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSelectedLibro({ ...selectedLibro, [name]: value });
  };

  /**
   * Envía los cambios del libro editado a la API y actualiza la lista de libros.
   */
  const handleUpdate = () => {
    fetch(`http://127.0.0.1:8000/api/v1/jparedes/libros/${selectedLibro.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        isbn: selectedLibro.isbn,
        titulo: selectedLibro.titulo,
        autor: selectedLibro.autor
      }),
    })
      .then(response => response.json())
      .then(updatedLibro => {
        setLibros(libros.map(libro => libro.id === updatedLibro.id ? updatedLibro : libro));
        handleModalClose();
      });
  };

  /**
   * Elimina un libro de la lista después de confirmar con el usuario.
   * @param {number} libroId - ID del libro a eliminar.
   */
  const handleDelete = (libroId) => {
    if (window.confirm("¿Estás seguro de que deseas eliminar este libro?")) {
      fetch(`http://127.0.0.1:8000/api/v1/jparedes/libros/${libroId}`, {
        method: 'DELETE',
      })
        .then(() => {
          setLibros(libros.filter(libro => libro.id !== libroId));
        });
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1>Bienvenido a la librería</h1>
      
      <button
        className="p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        onClick={() => router.push("/create_book")}
      >
        Crear libro
      </button>
      
      <table className="table-auto border-collapse border border-gray-400">
        <thead>
          <tr>
            <th className="border border-gray-400 px-4 py-2">ID</th>
            <th className="border border-gray-400 px-4 py-2">ISBN</th>
            <th className="border border-gray-400 px-4 py-2">Título</th>
            <th className="border border-gray-400 px-4 py-2">Autor</th>
            <th className="border border-gray-400 px-4 py-2">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {libros.map((libro) => (
            <tr key={libro.id}>
              <td className="border border-gray-400 px-4 py-2">{libro.id}</td>
              <td className="border border-gray-400 px-4 py-2">{libro.isbn}</td>
              <td className="border border-gray-400 px-4 py-2">{libro.titulo}</td>
              <td className="border border-gray-400 px-4 py-2">{libro.autor}</td>
              <td className="border border-gray-400 px-4 py-2">
                <button onClick={() => handleEditClick(libro)} className="text-blue-500 mr-2">✏️</button>
                <button onClick={() => handleDelete(libro.id)} className="text-red-500">🗑️</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {isModalOpen && (
        <div className="fixed inset-0 bg-opacity-50 flex items-center justify-center">
          <div className="bg-gray-800 p-8 rounded shadow-lg">
            <h2 className="text-lg font-bold mb-4">Editar Libro</h2>
            <input type="text" name="isbn" value={selectedLibro.isbn} onChange={handleInputChange} className="w-full border border-gray-300 px-3 py-2 rounded mb-4" />
            <input type="text" name="titulo" value={selectedLibro.titulo} onChange={handleInputChange} className="w-full border border-gray-300 px-3 py-2 rounded mb-4" />
            <input type="text" name="autor" value={selectedLibro.autor} onChange={handleInputChange} className="w-full border border-gray-300 px-3 py-2 rounded mb-4" />
            <div className="flex justify-end">
              <button onClick={handleModalClose} className="mr-4 px-4 py-2 bg-gray-600 rounded">Cancelar</button>
              <button onClick={handleUpdate} className="px-4 py-2 bg-blue-500 text-white rounded">Guardar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

Y para el formulario se creo una archivo en `/app/create_book/page.js`

```react
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
```