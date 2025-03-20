# La herramienta `pytest`

`pytest` es una herramienta poderosa y sencilla para ejecutar pruebas en Python. Aquí te explicamos cómo usarla a través del comando `uv run pytest` con algunos ejemplos prácticos. 🚀

## Ejemplos de uso

### 1. Correr `pytest` sin argumentos

```bash
uv run pytest
```

Esto ejecutará **todas las pruebas** que encuentre en tu proyecto. 🧹 Es como decirle a `pytest`: "¡Limpia todo y encuentra cualquier problema!". Busca automáticamente archivos que comiencen con `test_` o funciones que comiencen con `test`.

---

### 2. Correr `pytest` en un directorio específico

```bash
uv run pytest tests/mi_modulo
```

Si solo quieres ejecutar las pruebas de un directorio en particular, indícale la ruta. Por ejemplo, `tests/mi_modulo`. 🗂️ `pytest` buscará archivos que empiecen con `test_` en ese directorio y ejecutará las pruebas que encuentre. ¡Es como enviar un dron a explorar solo una parte del mapa! 🚁

---

### 3. Correr una prueba específica

```bash
uv run pytest tests/test_ejemplo py::test_funcion_especifica
```

¿Solo quieres probar una función en particular? 🧐 Usa la ruta al archivo y el nombre de la función de prueba, separados por `::`. Esto es útil cuando estás depurando algo muy específico. ¡Es como apuntar con un láser a tu objetivo! 🎯

---

### 4. Correr una prueba con `--pdb` para depurar errores

```bash
uv run pytest --pdb
```

Si algo falla y necesitas investigar, usa la opción `--pdb`. 🐛 Esto abrirá un depurador interactivo justo donde ocurrió el error. Es como tener una lupa para examinar cada detalle. 🔍 ¡Detective mode activado! 🕵️‍♂️

---

¡Y listo! Ahora tienes las herramientas para usar `pytest` como un profesional. Recuerda: las pruebas no son aburridas, son tu escudo contra errores inesperados. 🛡️ ¡A probar se ha dicho! 🎉

