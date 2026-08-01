let formAdd = document.getElementById("agregarCarro");

////////////// Agregar un carro
formAdd.addEventListener("submit", async (e) => {
    e.preventDefault();

    let marca = e.target.elements["marca"].value;
    let modelo = e.target.elements["modelo"].value;
    let año = e.target.elements["year"].value;
    let color = e.target.elements["color"].value;


    if (!marca || !modelo || !año || !color) {
        console.log("Llena todos los campos correctamente");
    } else {


        let carro_type = {
            entrada: "entrada",
            salida: "salida"
        }


        let response = await fetch(`http://localhost:8000/api/v1/fcalzada/registro_carro/registro/${carro_type.entrada}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                marca: marca,
                modelo: modelo,
                año: año,
                color: color
            })
        });


        if (!response.ok) {
            console.log("Hubo un error con la comunicacion de la API");
        } else {

            let responseJSON = await response.json();

            console.log(`Esto es lo que me respondio mi API con python:${responseJSON}`);


        }
    }



});



//////////////////////////////////////////////////////////////////////////// Eliminar carro
let formDelete = document.getElementById("eliminarCarro");


formDelete.addEventListener("submit", async (e) => {
    e.preventDefault();

    let carroId = e.target.elements["carroId"].value;


    if (!carroId) {
        console.log("El campo ID es olbigatorio");
    }
    else {

        if (carroId <= 0) {
            console.log("El ID del carro debe ser un numero superior a 1");
        }
        else {

            // Si llegamos aqui es porque todo salio bien, toca mandar a llamar a la API/////////////////////////////////////////////////////////////////////////////////////////

            let response = await fetch(`http://localhost:8000/api/v1/fcalzada/registro_carro/eliminar/${carroId}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            });


            if (!response.ok) {
                console.log("Hubo un error con la comunicacion de la API");
            }
            else {

                let responseJSON = await response.json();

                console.log(responseJSON);
            }
        }
    }



})


/////////////////////////////////////////////////////////////////////// Mostrar lista de carros
let cargarCarros = document.getElementById("cargarCarros");

cargarCarros.addEventListener("click", async (e) => {
    e.preventDefault();

    let response = await fetch("http://localhost:8000/api/v1/fcalzada/registro_carro/carros", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });

    if (!response.ok) {
        console.log("Hubo un error en la comunicacion con la API");
    } else {
        let responseJSON = await response.json();

        // Obtener el tbody de la tabla
        const tbody = document.querySelector("#carrosTable tbody");

        // Limpiar el contenido de la tabla antes de agregar nuevos carros
        tbody.innerHTML = '';

        // Recorrer la lista de carros y agregar cada uno como una fila en la tabla
        responseJSON.forEach(carro => {
            // Crear una fila para cada carro
            let carroRow = document.createElement('tr');

            // Crear celdas para cada propiedad del carro
            carroRow.innerHTML = `
                <td>${carro.id}</td>
                <td>${carro.marca}</td>
                <td>${carro.modelo}</td>
                <td>${carro.año}</td>
                <td>${carro.color}</td>
            `;

            // Agregar la fila al tbody
            tbody.appendChild(carroRow);
        });
    }
});

///////////////////////////////////////////////// EDITAR CARROS EDITAR CARROSEDITAR CARROS

let formEdit = document.getElementById("editarCarro");

formEdit.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Obtener los valores del formulario
    let id = e.target.elements["id"].value;
    let marca = e.target.elements["marca"].value;
    let modelo = e.target.elements["modelo"].value;
    let año = e.target.elements["year"].value;
    let color = e.target.elements["color"].value;

    if (!id || !marca || !modelo || !año || !color) {
        console.log("Todos los campos son obligatorios.");
        return;
    }

    // Hacer la solicitud PUT a la API
    let response = await fetch(`http://localhost:8000/api/v1/fcalzada/registro_carro/actualizar/${id}?marca=${marca}&modelo=${modelo}&año=${año}&color=${color}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        }
    });

    if (!response.ok) {
        console.log(`Error al modificar el carro con ID ${id}`);
    } else {
        let responseJSON = await response.json();
        console.log(`Carro modificado exitosamente:`, responseJSON);

        // Opcional: Actualizar la lista de carros después de editar
        document.getElementById("cargarCarros").submit();
    }
});