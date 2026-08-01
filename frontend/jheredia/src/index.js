/****************************************************************************
 * CONFIGURACIÓN Y CLASES
 ****************************************************************************/
const API_URL = "http://127.0.0.1:8000/api/v1/jheredia/registro_ciudades";

const CLASSES = {
  tableRow: "border-b last:border-0 hover:bg-gray-50",
  tableCell: "px-4 py-3 text-sm border-gray-200",
  tableHead: "px-4 py-3 bg-gray-200 text-gray-700 font-semibold border-b text-sm",
  button:
    "px-4 py-2 rounded text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
  editButton: "bg-blue-500 edit-btn",
  deleteButton: "bg-red-500 delete-btn",
  createButton: "bg-green-500",
};

let currentModalCallback = null;
let currentModalCityId = null;

/****************************************************************************
 * FUNCIONES DE API Y UTILIDAD
 ****************************************************************************/
function manejarError(mensaje, error) {
  console.error(`${mensaje}:`, error);
  alert(mensaje);
}

async function manejarSolicitud(url, opciones, mensajeError) {
  try {
    const response = await fetch(url, opciones);
    if (!response.ok) throw new Error(mensajeError);
    await obtenerCiudades(); // refrescar la tabla
  } catch (error) {
    manejarError(mensajeError, error);
  }
}

/**
 * Obtiene la lista de ciudades y las renderiza en la tabla
 */
async function obtenerCiudades() {
  try {
    const response = await fetch(`${API_URL}/ciudades`);
    if (!response.ok) throw new Error("Error al obtener las ciudades");
    const ciudades = await response.json();
    renderizarCiudades(ciudades);
  } catch (error) {
    manejarError("No se pudieron cargar las ciudades", error);
  }
}

/****************************************************************************
 * CREACIÓN, EDICIÓN, ELIMINACIÓN
 ****************************************************************************/

/** Crea una nueva ciudad mediante POST /registro/entrada */
function crearCiudad(ciudad) {
  manejarSolicitud(
    `${API_URL}/registro/entrada`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ciudad),
    },
    "Error al crear la ciudad"
  );
}

/** Edita una ciudad mediante PUT /actualizar/{city_id} */
function editarCiudad(cityId, ciudad) {
  manejarSolicitud(
    `${API_URL}/actualizar/${cityId}`,
    {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ciudad),
    },
    "Error al editar la ciudad"
  );
}

/** Elimina una ciudad mediante DELETE /eliminar/{city_id} */
function eliminarCiudad(cityId) {
  manejarSolicitud(
    `${API_URL}/eliminar/${cityId}`,
    { method: "DELETE" },
    "Error al eliminar la ciudad"
  );
}

/****************************************************************************
 * MODAL: APERTURA Y CIERRE
 ****************************************************************************/
function mostrarModal() {
  const modal = document.getElementById("modal-overlay");
  if (modal) modal.classList.remove("hidden");
}

function ocultarModal() {
  const modal = document.getElementById("modal-overlay");
  if (modal) modal.classList.add("hidden");

  // Limpia variables globales para evitar referencias colgadas
  currentModalCallback = null;
  currentModalCityId = null;
}

/****************************************************************************
 * CONFIGURAR FORMULARIO DEL MODAL
 ****************************************************************************/
function configurarModal(titulo, data = {}) {
  const modalTitle = document.getElementById("modal-title");
  const nameInput = document.getElementById("modal-name");
  const populationInput = document.getElementById("modal-population");
  const countryInput = document.getElementById("modal-country");
  const regionInput = document.getElementById("modal-region");
  const submitButton = document.getElementById("modal-submit");

  modalTitle.textContent = titulo;

  nameInput.value = data.name || "";
  populationInput.value = data.population || "";
  countryInput.value = data.country || "";
  regionInput.value = data.region || "";

  submitButton.textContent = titulo.includes("Crear") ? "Crear" : "Actualizar";
}

/**
 * Muestra el formulario para crear una nueva ciudad
 */
function mostrarFormularioCrear() {
  currentModalCallback = (_, ciudad) => crearCiudad(ciudad);
  configurarModal("Crear Ciudad");
  mostrarModal();
}

/**
 * Muestra el formulario de edición con la data precargada
 * @param {number} cityId - El identificador de la ciudad a editar
 */
function mostrarFormularioEditar(cityId) {
  fetch(`${API_URL}/ciudades`)
    .then((res) => res.json())
    .then((ciudades) => {
      // Buscamos la ciudad con city_id
      const ciudad = ciudades.find((c) => c.id === +cityId) || {};
      configurarModal("Editar Ciudad", {
        name: ciudad.name,
        population: ciudad.population,
        country: ciudad.country,
        region: ciudad.region,
      });

      currentModalCityId = cityId;
      currentModalCallback = (id, cityData) => editarCiudad(id, cityData);

      mostrarModal();
    })
    .catch((err) => manejarError("No se pudo obtener la ciudad para edición", err));
}

/****************************************************************************
 * RENDERIZACIÓN DE LA TABLA
 ****************************************************************************/
function renderizarCiudades(ciudades) {
  const tbody = document.getElementById("ciudades-table");
  tbody.innerHTML = "";

  ciudades.forEach((ciudad) => {
    const fila = document.createElement("tr");
    fila.className = CLASSES.tableRow;
    fila.innerHTML = `
      <td class="${CLASSES.tableCell}">${ciudad.id}</td>
      <td class="${CLASSES.tableCell}">${ciudad.name}</td>
      <td class="${CLASSES.tableCell}">${ciudad.population}</td>
      <td class="${CLASSES.tableCell}">${ciudad.country}</td>
      <td class="${CLASSES.tableCell}">${ciudad.region || "N/A"}</td>
      <td class="${CLASSES.tableCell}">
        <button 
          class="${CLASSES.button} ${CLASSES.editButton} mr-2" 
          data-city-id="${ciudad.id}"
        >
          Editar
        </button>
        <button 
          class="${CLASSES.button} ${CLASSES.deleteButton}" 
          data-city-id="${ciudad.id}"
        >
          Eliminar
        </button>
      </td>
    `;
    tbody.appendChild(fila);
  });

  // Vincular eventos a los botones
  document.querySelectorAll(".edit-btn").forEach((btn) =>
    btn.addEventListener("click", (e) => {
      const cityId = e.target.dataset.cityId;
      mostrarFormularioEditar(cityId);
    })
  );

  document.querySelectorAll(".delete-btn").forEach((btn) =>
    btn.addEventListener("click", (e) => {
      const cityId = e.target.dataset.cityId;
      eliminarCiudad(cityId);
    })
  );
}

/****************************************************************************
 * INICIALIZACIÓN DE LA APP
 ****************************************************************************/
function initApp() {
  const app = document.getElementById("app");
  if (app) {
    app.innerHTML = `
      <!-- Contenedor principal -->
      <div class="min-h-screen flex flex-col bg-gray-50 p-4">
        <!-- Sección Encabezado + Botón Crear -->
        <div class="flex flex-col items-center mb-6">
          <h1 class="text-3xl md:text-4xl font-bold text-blue-600 mb-4 text-center">
            Registro de Ciudades
          </h1>
          <button 
            id="crear-btn"
            class="${CLASSES.button} ${CLASSES.createButton} mb-2"
          >
            Crear Ciudad
          </button>
        </div>

        <!-- Contenedor de la Tabla -->
        <div class="flex justify-center">
          <div class="w-full max-w-5xl overflow-x-auto bg-white shadow-md rounded">
            <table class="table-auto w-full border-collapse">
              <thead>
                <tr>
                  <th class="${CLASSES.tableHead}">ID</th>
                  <th class="${CLASSES.tableHead}">Nombre</th>
                  <th class="${CLASSES.tableHead}">Población</th>
                  <th class="${CLASSES.tableHead}">País</th>
                  <th class="${CLASSES.tableHead}">Región</th>
                  <th class="${CLASSES.tableHead}">Acciones</th>
                </tr>
              </thead>
              <tbody id="ciudades-table"></tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Modal Overlay -->
      <div 
        id="modal-overlay" 
        class="fixed inset-0 bg-gray-800 bg-opacity-60 hidden items-center justify-center z-50"
      >
        <!-- Contenedor del Modal -->
        <div class="bg-white w-full max-w-md mx-4 rounded shadow-lg p-6 relative">
          <!-- Botón Cerrar Modal -->
          <button 
            id="modal-close" 
            class="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>

          <!-- Título dinámico (Crear/Editar) -->
          <h2 
            id="modal-title" 
            class="text-xl font-bold mb-4 text-center text-gray-700"
          ></h2>

          <!-- Formulario para Crear/Editar -->
          <form id="modal-form" class="space-y-4">
            <div>
              <label for="modal-name" class="block text-gray-700 mb-1 font-semibold">
                Nombre:
              </label>
              <input 
                type="text" 
                id="modal-name" 
                class="border px-3 py-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                required
              />
            </div>

            <div>
              <label for="modal-population" class="block text-gray-700 mb-1 font-semibold">
                Población:
              </label>
              <input 
                type="number" 
                id="modal-population"
                class="border px-3 py-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                required
              />
            </div>

            <div>
              <label for="modal-country" class="block text-gray-700 mb-1 font-semibold">
                País:
              </label>
              <input 
                type="text"
                id="modal-country"
                class="border px-3 py-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                required
              />
            </div>

            <div>
              <label for="modal-region" class="block text-gray-700 mb-1 font-semibold">
                Región (opcional):
              </label>
              <input 
                type="text"
                id="modal-region"
                class="border px-3 py-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </div>

            <button 
              id="modal-submit" 
              type="submit"
              class="${CLASSES.button} bg-blue-600 w-full mt-2"
            >
              <!-- Texto dinámico ("Crear" / "Actualizar") -->
            </button>
          </form>
        </div>
      </div>
    `;

    // Botón para abrir el modal "Crear Ciudad"
    document.getElementById("crear-btn").addEventListener("click", mostrarFormularioCrear);

    // Capturar el evento de envío del formulario en el modal
    document.addEventListener("submit", (e) => {
      if (e.target && e.target.id === "modal-form") {
        e.preventDefault();
        if (!currentModalCallback) return;

        const ciudad = {
          name: document.getElementById("modal-name").value,
          population: parseInt(document.getElementById("modal-population").value),
          country: document.getElementById("modal-country").value,
          region: document.getElementById("modal-region").value || null,
        };
        currentModalCallback(currentModalCityId, ciudad);
        ocultarModal();
      }
    });

    // Botón de cerrado del modal
    document.getElementById("modal-close").addEventListener("click", ocultarModal);

    // Cerrar modal al hacer clic en el fondo (opcional)
    const modalOverlay = document.getElementById("modal-overlay");
    modalOverlay.addEventListener("click", (e) => {
      if (e.target === modalOverlay) ocultarModal();
    });

    // Cargar la lista de ciudades al iniciar
    obtenerCiudades();
  }
}

initApp();