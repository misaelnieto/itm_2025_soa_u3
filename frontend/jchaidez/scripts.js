const API_URL = "http://localhost:8000/api/v1/jchaidez/cursos";

document.getElementById("curso-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const nombre = document.getElementById("nombre").value;
    const descripcion = document.getElementById("descripcion").value;
    const maestro = document.getElementById("maestro").value;

    try {
        const response = await fetch(`${API_URL}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, descripcion, maestro })
        });
        if (!response.ok) throw new Error("Error al agregar el curso");
        cargarCursos();
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
});

async function cargarCursos() {
    const response = await fetch(`${API_URL}`);
    if (!response.ok) {
        console.error("Error al cargar los cursos:", response.statusText);
        return;
    }
    const cursos = await response.json();
    const lista = document.getElementById("cursos-list");
    lista.innerHTML = "";  // Limpiar la tabla antes de agregar los nuevos cursos

    cursos.forEach(curso => {
        const tr = document.createElement("tr");  // Crear una nueva fila para cada curso

        // Crear celdas para el ID, Nombre, Descripción y Maestro
        const tdId = document.createElement("td");
        tdId.textContent = curso.id;

        const tdNombre = document.createElement("td");
        tdNombre.textContent = curso.nombre;

        const tdDescripcion = document.createElement("td");
        tdDescripcion.textContent = curso.descripcion;

        const tdMaestro = document.createElement("td");
        tdMaestro.textContent = curso.maestro;

        // Crear las acciones (eliminar y actualizar)
        const tdAcciones = document.createElement("td");
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Eliminar";
        deleteButton.addEventListener("click", () => eliminarCurso(curso.id));

        const updateButton = document.createElement("button");
        updateButton.textContent = "Actualizar";
        updateButton.addEventListener("click", () => actualizarCurso(curso.id));

        tdAcciones.appendChild(deleteButton);
        tdAcciones.appendChild(updateButton);

        // Agregar las celdas a la fila
        tr.appendChild(tdId);
        tr.appendChild(tdNombre);
        tr.appendChild(tdDescripcion);
        tr.appendChild(tdMaestro);
        tr.appendChild(tdAcciones);

        // Agregar la fila a la tabla
        lista.appendChild(tr);
    });
}


async function eliminarCurso(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE",
        });
        if (!response.ok) throw new Error("Error al eliminar el curso");
        cargarCursos();
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
}

async function actualizarCurso(id) {
    const nuevoNombre = prompt("Ingrese el nuevo nombre del curso:");
    const nuevaDescripcion = prompt("Ingrese la nueva descripción:");
    const nuevoMaestro = prompt("Ingrese el nuevo nombre del maestro:");

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nombre: nuevoNombre,
                descripcion: nuevaDescripcion,
                maestro: nuevoMaestro
            })
        });
        if (!response.ok) throw new Error("Error al actualizar el curso");
        cargarCursos();
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
}

cargarCursos();
