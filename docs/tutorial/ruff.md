# 🛠️ Análisis de código estático

El análisis de código estático es una técnica utilizada para examinar el código fuente sin ejecutarlo. Esto permite identificar errores, problemas de estilo, y posibles vulnerabilidades de seguridad antes de que el código sea ejecutado.

## 🚀 Uso de Ruff con `uv run`

El comando `uv run ruff check` ejecuta Ruff, una herramienta de análisis de código estático, para verificar el código en busca de problemas. Ruff es rápido y compatible con múltiples reglas de estilo y linters populares como Flake8.

### 📋 Pasos para ejecutar Ruff:

1. Ejecuta el comando:
   ```
   uv run ruff check
   ```
   Esto analizará los archivos de tu proyecto y generará un informe con los problemas encontrados.

2. 🛠️ Revisa el informe y corrige los problemas indicados.

## 📊 Ejemplo de salida

Al ejecutar el comando, podrías ver una salida como esta:

```
src/main.py:10:5: F841 Local variable 'x' is assigned but never used
src/utils.py:22:1: E302 Expected 2 blank lines, found 1
```

En este ejemplo:

- ⚠️ La primera línea indica que hay una variable no utilizada en `main.py`.
- 📝 La segunda línea señala un problema de formato en `utils.py`.

✅ Corrige estos problemas para mejorar la calidad y mantenibilidad de tu código.

## 🖥️ Uso de Ruff en Visual Studio Code

Para integrar Ruff en Visual Studio Code y aprovechar sus capacidades directamente en el editor, sigue estos pasos:

1. 🛒 Instala la extensión de Ruff desde el marketplace de Visual Studio Code.
2. ⚙️ Configura Ruff como el linter predeterminado en tu proyecto. Esto puede hacerse añadiendo lo siguiente al archivo `settings.json` de tu proyecto:
   ```json
   {
       "python.linting.enabled": true,
       "python.linting.ruffEnabled": true
   }
   ```
3. 📂 Abre cualquier archivo de tu proyecto y observa cómo Ruff resalta los problemas directamente en el editor.
4. ✍️ Corrige los problemas indicados para mejorar la calidad de tu código.

🎯 Esta integración permite identificar y solucionar problemas de manera más eficiente mientras trabajas en tu código.
