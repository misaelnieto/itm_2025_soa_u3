# 🚀 Paso 5 - Implementación de tu Proyecto

## 🌟 Introducción

En la unidad 2, escribiste un servicio web **SOAP** utilizando Python y la librería [Spyne](http://spyne.io/). En esta unidad, deberás reescribir ese servicio como una API **REST** usando la librería **FastAPI**.

### 🔄 Comparación entre SOAP y REST

| **Aspecto**            | **SOAP**                                                                 | **REST**                                                                 |
|-------------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| **Acrónimo** (significado) | Simple Object Access Protocol                                          | Representational State Transfer                                           |
| **Protocolo**           | Basado en XML y utiliza el protocolo **SOAP**.                          | Basado en **HTTP** y utiliza métodos estándar como `GET`, `POST`, `PUT`, `DELETE`, `HEAD` o `PATCH`. |
| **Formato de Datos**    | Exclusivamente **XML**.                                                 | Soporta múltiples formatos como **JSON**, **XML**, **HTML** y **texto plano**. |
| **Estandarización**     | Altamente estandarizado con reglas estrictas.                           | Más flexible y menos formal, lo que facilita su implementación.          |
| **Velocidad**           | Más lento debido al uso de XML y la sobrecarga del protocolo SOAP.       | Más rápido gracias a su simplicidad y uso de JSON.                       |
| **Compatibilidad**      | Ideal para sistemas empresariales complejos y altamente integrados.     | Ideal para aplicaciones web modernas y servicios ligeros.                |
| **Documentación**       | Utiliza **WSDL** (Web Services Description Language) para describir el servicio. | Utiliza **OpenAPI** o **Swagger** para documentar las APIs.              |
| **Estado**              | Es **stateful** (mantiene el estado entre solicitudes).                 | Es **stateless** (cada solicitud es independiente).                      |
| **Seguridad**           | Soporta estándares avanzados como **WS-Security**.                      | Depende de HTTPS y otros mecanismos como OAuth para la seguridad.        |
| **Facilidad de Uso**    | Más complejo de implementar y mantener.                                 | Más fácil de implementar y ampliamente adoptado.                         |

### 🚀 ¿Cuándo usarlo?

- Usa **SOAP** si necesitas interoperabilidad en sistemas empresariales complejos, heredados y con requisitos estrictos de seguridad y transacciones.
- Usa **REST** si buscas simplicidad, velocidad y compatibilidad con aplicaciones modernas.

---

### 🛠️ Herramientas Principales

#### `uv`

- **Descripción**: Es el administrador de paquetes que utilizamos para gestionar nuestro proyecto.
- **Documentación**: [uv Docs](https://docs.astral.sh/uv/)
- **Uso**: Nos permite ejecutar todas las herramientas del proyecto desde un solo lugar.

#### `python`

- **Descripción**: Es el lenguaje de programación principal que utilizaremos
  para desarrollar el proyecto y las pruebas.
- **Documentación**: [Python Docs](https://www.python.org/doc/)

#### [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/latest/) y [SQLModel](https://sqlmodel.tiangolo.com/)

- **Descripción**: Un framework moderno y de alto rendimiento para construir
  APIs REST con Python.
- **Características**:
  - Validación automática de datos (**Pydantic**)
  - Documentación interactiva (**FastAPI**)
  - Soporte para tipado estático (**Pydantic**)
  - Soporte de ORM (**SqlModel**)
- **Uso en el proyecto**: Usarás **FastAPI** para escribir las rutas del API REST de
  tu proyecto.

#### [SQLite](https://www.sqlite.org/index.html)

- **Descripción**: Es una base de datos ligera y embebida que no requiere configuración ni un servidor independiente. Es solamente un archivo que se guarda en el disco duro.
- **Uso en el proyecto**: Aunque no interactuarás directamente con **SQLite**, la usaremos como base de datos subyacente a través de la librería **SQLModel**. Esto nos permitirá almacenar y gestionar datos de manera eficiente mientras aprovechamos las capacidades ORM de **SQLModel**.
- **Características**:
  - No requiere instalación ni configuración adicional.
  - Ideal para proyectos pequeños y medianos.
  - Totalmente compatible con **SQLModel**.

#### [Pytest](https://docs.pytest.org/en/stable/)

- **Descripción**: Una librería de pruebas para Python bastante popular y sencilla con la que escribiras las pruebas de tu proyecto.
- **Características**:
  - Sintaxis clara y concisa.
  - Soporte para fixtures.
  - Amplia gama de plugins.
- **Uso en el proyecto**: Escribirás las pruebas de integración utilizando **Pytest**.


#### [httpx](https://www.python-httpx.org/)

- **Descripción**: Una librería de Python para realizar solicitudes HTTP,
  compatible con solicitudes síncronas y asíncronas.
- **Uso en el proyecto**: Usarás httpx para comunicarte con el framework en tus pruebas de integración del backend (FastAPI) y con tu frontend, si es que usas Python.

#### [Textual](https://textual.textualize.io/)

- **Descripción**: Una librería de Python para construir interfaces de usuario (UI) en la terminal.
- **Características**:
  - Usa Python (y un poco de CSS) para escribir UIs en modo texto, interactivas y dinámicas para la terminal (y la web tambien!!). La terminal aún no es obsoleta!!
  - No requiere bibliotecas gráficas o toolkits externos como QT, .NET, Gtk, etc.
  - Usa cualquier otra librería de Python que necesites.
- **Uso en el proyecto**: Puedes usar **Textual** para crear un frontend para tu proyecto. Si decides usar esta librería, te recomiendo que uses **httpx** para comunicarte con tu backend.

---

## Proyecto de referencia: Alcancía

Estudia el proyecto de referencia para que puedas ver un ejemplo simple de implementación de un API REST con FastAPI (backend) y su integración con una interfáz de usuario usando exclusivamente Python.

[Alcancía :pig2:](../proyectos/nnieto/index.md){ .md-button .md-button--primary .alcancia }

---

✨ ¡Con estas herramientas, tendrás todo lo necesario para implementar tu
proyecto de manera eficiente y profesional! Si tienes dudas, no olvides
consultar la documentación oficial de cada herramienta. 🚀

