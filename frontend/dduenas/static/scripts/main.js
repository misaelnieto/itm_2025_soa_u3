let formAdd = document.getElementById('createEstudiantes');

formAdd.addEventListener('submit', async(e) =>  {
    e.preventDefault();

    let nombre = e.target.elements["nombre"].value;
    let carrera = e.target.elements["carrera"].value;
    let fecha =  e.target.elements["fecha"].value;

    if(!nombre || !carrera || !fecha){
        console.log("Por favor, llene todos los campos");
    }else{

        let response = await fetch('http://localhost:8000/api/v1/dduenas/estudiantes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre: nombre,
                carrera: carrera,
                created_at:new Date(fecha).toISOString()
          })
        });

    if(!response.ok){
        console.log("Hubo un error con la comunicación de la API");
    }else{
        let responseJSON = await response.json();
        
        console.log(`Esto es lo que me respondio mi API con python: ${responseJSON.nombre}`);
        console.log(`Esto es lo que me respondio mi API con python: ${responseJSON.carrera}`);
        console.log(`Esto es lo que me respondio mi API con python: ${responseJSON.created_at}`);
    }
}
});

        let formDelete = document.getElementById('delete-student'); 

        formDelete.addEventListener('submit', async (e) =>{
            e.preventDefault();

            let ID = e.target.elements["id"].value;

            let response2;

            if(!ID){
                console.log("Por favor, llene todos los campos");
            }
            else{
                if(ID<=0){
                    console.log("El id debe ser mayor a 0");
                }
                else{
                    response2 = await fetch(`http://localhost:8000/api/v1/dduenas/estudiantes/${ID}`,{
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        }
            })


            if(!response2.ok){
                console.log("Hubo un error con la comunicacion de la API");
            }
            else{

                let responseJSON = await response2.json();
                console.log(`Esto es lo que me respondio mi API con python: ${responseJSON.message}`);
            }
        }
    }
});

let formUpdate = document.getElementById('update-student');

formUpdate.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Obtener los valores del formulario
    let id = e.target.elements["id"].value;
    let nombre = e.target.elements["nombre"].value;
    let carrera = e.target.elements["carrera"].value;
    let fecha = e.target.elements["fecha"].value;

    // Validar que todos los campos estén llenos
    if (!id || !nombre || !carrera || !fecha) {
        console.log("Por favor, llene todos los campos");
        return;
    }

    // Validar que el ID sea mayor a 0
    if (id <= 0) {
        console.log("El ID debe ser mayor a 0");
        return;
    }

    try {
        // Enviar la solicitud PUT a la API
        let response = await fetch(`http://localhost:8000/api/v1/dduenas/estudiantes/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre: nombre,
                carrera: carrera,
                created_at: new Date(fecha).toISOString()
            })
        });

        // Manejar la respuesta de la API
        if (!response.ok) {
            console.log("Hubo un error con la comunicación de la API");
        } else {
            let responseJSON = await response.json();
            console.log(`Estudiante actualizado: ${responseJSON.nombre}, ${responseJSON.carrera}, ${responseJSON.created_at}`);
        }
    } catch (error) {
        console.error("Error al actualizar el estudiante:", error);
    }
});




let cargarEstudiantes = document.getElementById("getEstudiantes");

cargarEstudiantes.addEventListener("submit", async (e) => {
    e.preventDefault();

    let response = await fetch("http://localhost:8000/api/v1/dduenas/estudiantes", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });

    if (!response.ok) {
        console.log("Hubo un error en la comunicación con la API");
    } else {
        let responseJSON = await response.json();

        console.log(responseJSON); // Asegúrate de que el JSON contenga una lista de estudiantes

        const contenedor = document.getElementById('contenedor-estudiantes'); // Asegúrate de tener un div con id="contenedor-estudiantes"

        // Limpiar el contenedor antes de agregar los estudiantes
        contenedor.innerHTML = '';

        // Crear la tabla y agregar encabezados (solo una vez)
        let tabla = document.createElement('table');
        tabla.classList.add('tabla-estudiantes'); // Clase para estilos (opcional)
        tabla.innerHTML = `
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Carrera</th>
                    <th>Fecha de creación</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        `;

        // Obtener el cuerpo de la tabla
        let tbody = tabla.querySelector('tbody');

        // Recorrer la lista de estudiantes y agregar cada uno como una fila
        responseJSON.forEach(estudiante => {
            let fila = document.createElement('tr');
            fila.innerHTML = `
                <td>${estudiante.id}</td>
                <td>${estudiante.nombre}</td>
                <td>${estudiante.carrera}</td>
                <td>${new Date(estudiante.created_at).toLocaleDateString()}</td>
            `;
            tbody.appendChild(fila);
        });

        // Agregar la tabla al contenedor (solo una vez)
        contenedor.appendChild(tabla);
    }
    });





