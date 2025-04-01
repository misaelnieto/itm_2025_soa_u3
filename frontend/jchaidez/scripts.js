const API_URL = "http://localhost:8000/api/v1/jchaidez/cursos";

document.getElementById("curso-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const nombre = document.getElementById("nombre").value;
    const descripcion = document.getElementById("descripcion").value;
    const maestro = document.getElementById("maestro").value;
    
    if (!nombre || !descripcion || !maestro) {
        alert("Todos los campos son obligatorios");
        return;
    }

    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, descripcion, maestro })
    });
    if (response.ok) {
        cargarCursos();
        document.getElementById("curso-form").reset();
    }
});

async function cargarCursos() {
    const response = await fetch(API_URL);
    const cursos = await response.json();
    const tabla = document.getElementById("cursos-list");
    tabla.innerHTML = "";
    cursos.forEach(curso => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${curso.id}</td>
            <td contenteditable="true" class="editable">${curso.nombre}</td>
            <td contenteditable="true" class="editable">${curso.descripcion}</td>
            <td contenteditable="true" class="editable">${curso.maestro}</td>
            <td>
                <button onclick="guardarEdicion(${curso.id}, this)">Guardar</button>
                <button onclick="eliminarCurso(${curso.id})">Eliminar</button>
            </td>
        `;
        tabla.appendChild(fila);
    });
}

async function guardarEdicion(id, boton) {
    const fila = boton.parentElement.parentElement;
    const nombre = fila.children[1].textContent.trim();
    const descripcion = fila.children[2].textContent.trim();
    const maestro = fila.children[3].textContent.trim();
    
    if (!nombre || !descripcion || !maestro) {
        alert("Todos los campos deben estar llenos");
        return;
    }
    
    const response = await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, descripcion, maestro })
    });
    
    if (response.ok) {
        alert("Curso actualizado correctamente");
        cargarCursos();
    }
}

async function eliminarCurso(id) {
    if (confirm("¿Estás seguro de que deseas eliminar este curso?")) {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE",
        });
        if (response.ok) {
            cargarCursos();
        }
    }
}

cargarCursos();
