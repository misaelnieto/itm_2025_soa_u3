# La herramienta `fastapi` 🚀

## Uso de la línea de comandos 💻

FastAPI ofrece comandos útiles para ejecutar y desarrollar aplicaciones web. A continuación, se describen dos comandos principales:

### `uv run fastapi dev` 🛠️

Este comando inicia el servidor en **modo de desarrollo**. En este modo, el servidor se reinicia automáticamente cada vez que detecta cambios en el código. Esto es ideal para el desarrollo activo, ya que permite probar cambios rápidamente sin necesidad de reiniciar manualmente el servidor.

### `uv run fastapi run` 🏭

Este comando inicia el servidor en **modo de producción**. En este modo, el servidor no se reinicia automáticamente y está optimizado para manejar solicitudes en un entorno de producción. Es más eficiente y estable, pero no incluye la recarga automática del modo de desarrollo.

### Diferencias clave 🔑

- **Modo de desarrollo (`dev`)**: 🔄 Recarga automática, ideal para desarrollo.
- **Modo de producción (`run`)**: 🚀 Sin recarga automática, optimizado para producción.

### Problemas con FastAPI en Windows Terminal ⚠️

!!! tip 

    A veces, las herramientas que corren en Python, como FastAPI, no terminan su ejecución al presionar `Ctrl + C` en la Terminal de Windows. 🖥️ Si esto te sucede, la solución es finalizar el proceso de Python desde el Administrador de Tareas de Windows. 🛑

    Este problema no parece ocurrir en macOS y Linux, pero puede ser bastante molesto para los usuarios de Windows. 😓