$(document).ready(function(){
    var apiURL = "http://127.0.0.1:8000/api/v1/rpalma/contactos"; // Cambia por tu API real

    var actionsView = 
    '<a class="edit" title="Editar" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a>' +
    '<a class="delete" title="Eliminar" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a>';

    var actionsAdd = 
        '<a class="add" title="Guardar" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a>' +
        '<a class="delete" title="Eliminar" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a>';

    var actionsEdit = 
        '<a class="save" title="Guardar Cambios" data-toggle="tooltip"><i class="material-icons">&#xE161;</i></a>' +
        '<a class="delete" title="Eliminar" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a>';
    
        function mostrarMensaje(mensaje, tipo) {
        let messageDiv = $("#message");
        messageDiv.removeClass("alert-success alert-danger").addClass(tipo);
        messageDiv.text(mensaje).fadeIn();

        if (tipo=="alert-success"){
            setTimeout(function() {
                messageDiv.fadeOut();
            }, 3000);
        }

        $(document).ready(function(){
            $('[data-toggle="tooltip"]').tooltip();
            
            // Append table with add row form on add new button click
            $(".btn_new").click(function(){
                var index = $("table tbody tr:last-child").index();
                var row = '<tr>' +
                    '<td><input type="text" class="form-control disabled" name="id" id="id"></td>' +
                    '<td><input type="text" class="form-control" name="nombre" id="nombre"></td>' +
                    '<td><input type="text" class="form-control" name="telefono" id="telefono"></td>' +
                    '<td><input type="text" class="form-control" name="correo" id="correo"></td>' +
                    '<td>' + actions + '</td>' +
                '</tr>';
                $("table").append(row);		
                $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
                $('[data-toggle="tooltip"]').tooltip();
            });
        
        });
        
    }

    function cargarDatos() {
        $.ajax({
            url: `${apiURL}/agenda`, // Endpoint de la API
            type: "GET",
            dataType: "json",
            success: function(response) {
                console.log("✅ Respuesta de la API:", response);
                $("table tbody").empty();

                if (!Array.isArray(response)) {
                    console.error("⚠️ La API no devolvió un array:", response);
                    mostrarMensaje("⚠️ Error: Respuesta inesperada del servidor", "alert-danger");
                    return;
                }

                var data = response.data || response;

                $.each(data, function(index, item) {
                    var row = `<tr>
                        <td>${item.id}</td>
                        <td>${item.nombre}</td>
                        <td>${item.telefono}</td>
                        <td>${item.correo}</td>
                        <td>${actionsView}</td>
                    </tr>`;
                    $("table tbody").append(row);
                });

                $(".buscador_addNew").removeClass("disabled"); /*habilitar el buscador y el boton de agregar nuevo*/

                $('[data-toggle="tooltip"]').tooltip(); // Reactivar tooltips si los usas
                mostrarMensaje("✅ Datos cargados correctamente", "alert-success");
            },
            error: function(xhr, status, error) {
                console.error("Error al obtener los datos:", xhr.status, xhr.statusText, xhr.responseText);
                mostrarMensaje(`❌ Error al obtener los datos: ${xhr.status} - ${xhr.statusText}`, "alert-danger");
            }
        });
    }

    function buscarContacto() {
        const nombre = $("#searchInput").val().trim(); // Obtén el valor del input de búsqueda
    
        if (!nombre) {
            mostrarMensaje("⚠️ Por favor, ingresa un nombre para buscar.", "alert-danger");
            return;
        }
    
        $.ajax({
            url: `${apiURL}/search/${nombre}`, // Endpoint de búsqueda
            type: "GET",
            dataType: "json",
            success: function(response) {
                console.log("✅ Respuesta de la API de búsqueda:", response);
                $("table tbody").empty();
    
                if (!response.agenda || response.agenda.length === 0) {
                    mostrarMensaje("⚠️ No se encontraron contactos con ese nombre.", "alert-warning");
                    return;
                }
    
                $.each(response.agenda, function(index, item) {
                    var row = `<tr>
                        <td>${item.id}</td>
                        <td>${item.nombre}</td>
                        <td>${item.telefono}</td>
                        <td>${item.correo}</td>
                        <td>${actionsView}</td>
                    </tr>`;
                    $("table tbody").append(row);
                });
    
                $('[data-toggle="tooltip"]').tooltip(); // Reactivar tooltips si los usas
                mostrarMensaje("✅ Contactos encontrados.", "alert-success");
            },
            error: function(xhr, status, error) {
                console.error("Error al buscar el contacto:", xhr.status, xhr.statusText, xhr.responseText);
                mostrarMensaje(`❌ Error al buscar el contacto: ${xhr.status} - ${xhr.statusText}`, "alert-danger");
            }
        });
    }
    
    // Asocia el evento al botón de búsqueda
    $(document).on("click", "#searchButton", buscarContacto);

    // Exponer la función globalmente
    window.cargarDatos = cargarDatos;

    $(document).on("click", ".add", function () {
        $(this).tooltip('dispose'); // Elimina el tooltip del botón específico para que no se quede flotando al borrar la fila
        const row = $(this).closest("tr"); // Obtén la fila actual
        const nombre = row.find("td").eq(1).find("input").val()?.trim(); // Obtén el valor del input de nombre
        const telefono = row.find("td").eq(2).find("input").val()?.trim(); // Obtén el valor del input de teléfono
        const correo = row.find("td").eq(3).find("input").val()?.trim(); // Obtén el valor del input de correo
    
        // Validar que los campos requeridos no estén vacíos
        if (!nombre || !telefono) {
            mostrarMensaje("⚠️ Nombre y Teléfono son campos requeridos.", "alert-danger");
            return;
        }
    
        // Realizar la solicitud POST para agregar un nuevo contacto
        $.ajax({
            url: `${apiURL}/create`, // Endpoint para crear un contacto
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                nombre: nombre,
                telefono: telefono,
                correo: correo,
            }),
            success: function (response) {
                console.log("✅ Contacto creado:", response);
                mostrarMensaje("✅ Contacto creado correctamente.", "alert-success");
                cargarDatos();
            },


            error: function (xhr, status, error) {
                console.error("Error al crear el contacto:", xhr.status, xhr.statusText, xhr.responseText);
                mostrarMensaje(`❌ Error al crear el contacto: ${xhr.status} - ${xhr.statusText} - ${xhr.responseText}`, "alert-danger");
            },

        })
    });

    $(document).on("click", ".edit", function () {
        const row = $(this).closest("tr"); // Obtén la fila actual
        $(this).tooltip('dispose'); // Elimina el tooltip del botón específico para que no se quede flotando al borrar la fila
        // Iterar sobre las columnas de la fila
        row.find("td:not(:last-child)").each(function (index) {
            const text = $(this).text(); // Obtén el texto actual de la celda
    
            if (index === 0) {
                // Si es la primera columna (ID), deshabilitar el input
                $(this).html(`<input type="text" class="form-control" value="${text}" disabled>`);
            } else {
                // Para las demás columnas, habilitar el input con el valor actual
                $(this).html(`<input type="text" class="form-control" value="${text}">`);
            }
        });
    
        // Alternar los botones de edición y guardar
        row.find("td").eq(4).html(actionsEdit);

    });

    $(document).on("click", ".save", function () {
        const row = $(this).closest("tr"); // Obtén la fila actual
        const id = row.find("td").eq(0).find("input").val()?.trim() || row.find("td").eq(0).text().trim(); // Obtén el ID del contacto
        const nombre = row.find("td").eq(1).find("input").val()?.trim(); // Obtén el valor del input de nombre
        const telefono = row.find("td").eq(2).find("input").val()?.trim(); // Obtén el valor del input de teléfono
        const correo = row.find("td").eq(3).find("input").val()?.trim(); // Obtén el valor del input de correo
    
        // Validar que los campos requeridos no estén vacíos
        if (!nombre || !telefono) {
            mostrarMensaje("⚠️ Nombre y Teléfono son campos requeridos.", "alert-danger");
            return;
        }
    
        // Realizar la solicitud PUT para guardar los cambios
        $.ajax({
            url: `${apiURL}/edit/${id}`, // Endpoint para editar un contacto
            type: "PUT",
            contentType: "application/json",
            data: JSON.stringify({
                nombre: nombre,
                telefono: telefono,
                correo: correo,
            }),
            success: function (response) {
                console.log("✅ Contacto actualizado:", response);
                mostrarMensaje("✅ Contacto actualizado correctamente.", "alert-success");
                cargarDatos();
            },
            error: function (xhr, status, error) {
                console.error("Error al actualizar el contacto:", xhr.status, xhr.statusText, xhr.responseText);
                mostrarMensaje(`❌ Error al actualizar el contacto: ${xhr.status} - ${xhr.statusText} - ${xhr.responseText}`, "alert-danger");
            },
        });
        row.find("td").eq(4).html(actionsView);
    });

    $(document).on("click", ".delete", function () {
        const row = $(this).closest("tr"); // Obtén la fila actual
        const id = row.find("td").eq(0).text().trim(); // Obtén el ID del contacto
        
        // Confirmar antes de eliminar
        if (!confirm("¿Estás seguro de que deseas eliminar este contacto?")) {
            return;
        }
        $(this).tooltip('dispose'); // Elimina el tooltip del botón específico para que no se quede flotando al borrar la fila
    
        // Realizar la solicitud DELETE para eliminar el contacto
        $.ajax({
            url: `${apiURL}/delete/${id}`, // Endpoint para eliminar un contacto
            type: "DELETE",
            success: function (response) {
                console.log("✅ Contacto eliminado:", response);
                mostrarMensaje("✅ Contacto eliminado correctamente.", "alert-success");
                cargarDatos();
            },
            error: function (xhr, status, error) {
                console.error("Error al eliminar el contacto:", xhr.status, xhr.statusText, xhr.responseText);
                mostrarMensaje(`❌ Error al eliminar el contacto: ${xhr.status} - ${xhr.statusText} - ${xhr.responseText}`, "alert-danger");
            }
        });


    });

});
