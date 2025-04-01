$(document).ready(function(){
    var apiURL = "http://localhost:8000/api/v1/jcontreras/ventas/";

    function mostrarMensaje(mensaje, tipo) {
        let messageDiv = $("#message");
        messageDiv.removeClass("alert-success alert-danger alert-warning").addClass(tipo);
        messageDiv.text(mensaje).fadeIn();

        if (tipo === "alert-success") {
            setTimeout(function() {
                messageDiv.fadeOut();
            }, 3000);
        }
    }

    function cargarDatos() {
        fetch(apiURL)
            .then(response => response.json())
            .then(data => {
                $("table tbody").empty();
                if (!Array.isArray(data) || data.length === 0) {
                    mostrarMensaje("⚠️ No hay ventas registradas.", "alert-warning");
                } else {
                    data.forEach(item => {
                        var row = `<tr data-id="${item.id}">
                            <td>${item.id}</td>
                            <td class="cliente">${item.cliente}</td>
                            <td class="producto">${item.producto}</td>
                            <td class="cantidad">${item.cantidad}</td>
                            <td class="precio">${item.precio}</td>
                            <td>
                                <a class="edit" data-id="${item.id}" title="Editar">
                                    <i class="material-icons">edit</i>
                                </a>
                                <a class="delete" data-id="${item.id}" title="Eliminar">
                                    <i class="material-icons">&#xE872;</i>
                                </a>
                            </td>
                        </tr>`;
                        $("table tbody").append(row);
                    });
                    mostrarMensaje("✅ Ventas cargadas correctamente", "alert-success");
                }
            })
            .catch(error => {
                mostrarMensaje(`❌ Error al obtener los datos: ${error}`, "alert-danger");
            });
    }

    function agregarVenta(event) {
        event.preventDefault();

        const cliente = $("#cliente").val().trim();
        const producto = $("#producto").val().trim();
        const cantidad = parseInt($("#cantidad").val());
        const precio = parseFloat($("#precio").val());

        if (!cliente || !producto || isNaN(cantidad) || isNaN(precio)) {
            mostrarMensaje("⚠️ Todos los campos son requeridos.", "alert-danger");
            return;
        }

        fetch(apiURL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cliente, producto, cantidad, precio }),
        })
        .then(response => response.json())
        .then(() => {
            mostrarMensaje("✅ Venta creada correctamente.", "alert-success");
            cargarDatos();
        })
        .catch(error => {
            mostrarMensaje(`❌ Error al crear la venta: ${error}`, "alert-danger");
        });
    }

    $(document).on("click", ".delete", function () {
        const id = $(this).data("id");
        if (!confirm("¿Estás seguro de eliminar esta venta?")) return;

        fetch(`${apiURL}/${id}`, { method: "DELETE" })
        .then(() => {
            mostrarMensaje("✅ Venta eliminada correctamente.", "alert-success");
            cargarDatos();
        })
        .catch(error => {
            mostrarMensaje(`❌ Error al eliminar la venta: ${error}`, "alert-danger");
        });
    });

    $(document).on("click", ".edit", function () {
        const id = $(this).data("id");
        const row = $(`tr[data-id='${id}']`);

        const cliente = row.find(".cliente").text();
        const producto = row.find(".producto").text();
        const cantidad = row.find(".cantidad").text();
        const precio = row.find(".precio").text();

        $("#cliente").val(cliente);
        $("#producto").val(producto);
        $("#cantidad").val(cantidad);
        $("#precio").val(precio);

        $("#formVenta").off("submit").on("submit", function (event) {
            event.preventDefault();
            modificarVenta(id);
        });
    });

    function modificarVenta(id) {
        const cliente = $("#cliente").val().trim();
        const producto = $("#producto").val().trim();
        const cantidad = parseInt($("#cantidad").val());
        const precio = parseFloat($("#precio").val());

        if (!cliente || !producto || isNaN(cantidad) || isNaN(precio)) {
            mostrarMensaje("⚠️ Todos los campos son requeridos.", "alert-danger");
            return;
        }

        fetch(`${apiURL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cliente, producto, cantidad, precio }),
        })
        .then(response => response.json())
        .then(() => {
            mostrarMensaje("✅ Venta actualizada correctamente.", "alert-success");
            cargarDatos();
            $("#formVenta").off("submit").on("submit", agregarVenta);
            $("#formVenta")[0].reset();
        })
        .catch(error => {
            mostrarMensaje(`❌ Error al modificar la venta: ${error}`, "alert-danger");
        });
    }

    $("#formVenta").on("submit", agregarVenta);
    cargarDatos();
});
