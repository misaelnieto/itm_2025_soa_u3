# Como se creo el frontend

Se uso el framework de Next.js y se crea con el siguiente comando

npm npx create-next-app@latest dramos

Se ejecuta con:

npm run dev

La pagina principal de este framework se encuentra en /app/page.js

'use client';
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

/**
 * Componente principal que maneja la visualización, edición y eliminación de productos.
 */
export default function Home() {
  const [productos, setProductos] = useState([]); // Estado para almacenar la lista de productos
  const [isModalOpen, setIsModalOpen] = useState(false); // Estado para controlar la visibilidad del modal de edición
  const [selectedProducto, setSelectedProducto] = useState(null); // Estado para almacenar el producto seleccionado para edición
  const router = useRouter();

  /**
   * Obtiene la lista de productos desde la API al cargar el componente.
   */
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/dramos/productos/')
      .then(response => response.json())
      .then(data => setProductos(data));
  }, []);

  /**
   * Maneja la apertura del modal de edición con los datos del producto seleccionado.
   * @param {Object} producto - Objeto que representa el producto seleccionado.
   */
  const handleEditClick = (producto) => {
    setSelectedProducto(producto);
    setIsModalOpen(true);
  };

  /**
   * Cierra el modal de edición y resetea el producto seleccionado.
   */
  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedProducto(null);
  };

  /**
   * Maneja el cambio en los campos del formulario de edición.
   * @param {Event} e - Evento de cambio en los inputs.
   */
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSelectedProducto({ ...selectedProducto, [name]: value });
  };

  /**
   * Envía los cambios del producto editado a la API y actualiza la lista de productos.
   */
  const handleUpdate = () => {
    fetch(`http://127.0.0.1:8000/api/v1/dramos/productos/${selectedProducto.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        nombre: selectedProducto.nombre,
        tipo: selectedProducto.tipo,
        precio: selectedProducto.precio,
      }),
    })
      .then(response => response.json())
      .then(updatedProducto => {
        setProductos(productos.map(producto => producto.id === updatedProducto.id ? updatedProducto : producto));
        handleModalClose();
      });
  };

  /**
   * Elimina un producto de la lista después de confirmar con el usuario.
   * @param {number} productoId - ID del producto a eliminar.
   */
  const handleDelete = (productoId) => {
    if (window.confirm("¿Estás seguro de que deseas eliminar este producto?")) {
      fetch(`http://127.0.0.1:8000/api/v1/dramos/productos/${productoId}`, {
        method: 'DELETE',
      })
        .then(() => {
          setProductos(productos.filter(producto => producto.id !== productoId));
        });
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1>Bienvenido a la tienda de abarrotes</h1>
      
      <button
        className="p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        onClick={() => router.push("/crearProducto")}
      >
        Crear producto
      </button>
      
      <table className="table-auto border-collapse border border-gray-400">
        <thead>
          <tr>
            <th className="border border-gray-400 px-4 py-2">ID</th>
            <th className="border border-gray-400 px-4 py-2">Nombre</th>
            <th className="border border-gray-400 px-4 py-2">Tipo</th>
            <th className="border border-gray-400 px-4 py-2">Precio</th>
          </tr>
        </thead>
        <tbody>
          {productos.map((producto) => (
            <tr key={producto.id}>
              <td className="border border-gray-400 px-4 py-2">{producto.id}</td>
              <td className="border border-gray-400 px-4 py-2">{producto.nombre}</td>
              <td className="border border-gray-400 px-4 py-2">{producto.tipo}</td>
              <td className="border border-gray-400 px-4 py-2">{producto.precio}</td>
              <td className="border border-gray-400 px-4 py-2">
                <button onClick={() => handleEditClick(producto)} className="text-blue-500 mr-2">✏️</button>
                <button onClick={() => handleDelete(producto.id)} className="text-red-500">🗑️</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {isModalOpen && (
        <div className="fixed inset-0 bg-opacity-50 flex items-center justify-center">
          <div className="bg-gray-800 p-8 rounded shadow-lg">
            <h2 className="text-lg font-bold mb-4">Editar Producto</h2>
            <input type="text" name="nombre" value={selectedProducto.nombre} onChange={handleInputChange} className="w-full border border-gray-300 px-3 py-2 rounded mb-4" />
            <input type="text" name="tipo" value={selectedProducto.tipo} onChange={handleInputChange} className="w-full border border-gray-300 px-3 py-2 rounded mb-4" />
            <input type="number" name="precio" value={selectedProducto.precio} onChange={handleInputChange} className="w-full border border-gray-300 px-3 py-2 rounded mb-4" />
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

Y para el formulario se creo una archivo en /app/crearProducto/page.js

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
    if (!validateFields()) return; // Si la validación falla, no se envía la solicitud
    
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
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1>Añade tu producto</h1>
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