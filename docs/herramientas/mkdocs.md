# La herramienta mkdocs

## 🌐 Uso del comando `mkdocs`

El comando `uv run mkdocs serve -a localhost:8002` se utiliza para iniciar un servidor local que permite visualizar la documentación generada con MkDocs en tiempo real. 🚀

### 📌 Detalles importantes:

- **Puerto 8002**: Usamos este puerto para evitar conflictos con la herramienta FastAPI, que normalmente corre en el puerto 8000. ⚙️
- **Dirección local**: La documentación estará disponible en `http://localhost:8002`.

Este comando es especialmente útil durante el desarrollo, ya que cualquier cambio en los archivos de documentación se reflejará automáticamente en el navegador. 🔄

