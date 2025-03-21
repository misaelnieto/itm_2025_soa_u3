# Paso 3: Repositorio 🚀

## Clona el repositorio 🖥️

Primero, necesitas clonar el repositorio en tu máquina local. Abre una terminal de PowerShell y ejecuta los siguientes comandos:

```powershell
git clone git@github.com:misaelnieto/itm_2025_soa_u3.git
cd itm_2025_soa_u3
git switch --create fferndez-servicioweb
```

!!! tip "Consejo"
    Asegúrate de tener configurada tu clave SSH en GitHub antes de clonar el repositorio. Si no lo has hecho, consulta la [documentación oficial de GitHub](https://docs.github.com/es/authentication/connecting-to-github-with-ssh).

---

## Crea tu rama de trabajo 🌿

Es importante trabajar en una rama separada para mantener el repositorio organizado. De preferencia, usa el nombre de tu módulo y tu servicio web para nombrar tu rama. Por ejemplo:

- Si tu módulo de trabajo es `ffernandez` y tu servicio web se llama `Perritos`, tu rama podría llamarse `ffernandez-perritos`.

Para crear y cambiarte a tu nueva rama, ejecuta:

```powershell
git switch --create ffernandez-perritos
```

Luego, registra tu rama en GitHub con el siguiente comando:

```powershell
git push --set-upstream origin ffernandez-perritos
```

!!! note "Nota"
    A partir de ahora, solo necesitarás escribir `git push` para subir los cambios de tu rama a GitHub.

---

## Verifica tu configuración ✅

Antes de comenzar a trabajar, verifica que todo esté configurado correctamente:

```powershell
git status
```

Esto debería mostrar que estás en tu nueva rama y que no hay cambios pendientes.

!!! warning "Advertencia"
    No trabajes directamente en la rama `main`. Siempre utiliza tu rama de trabajo para evitar conflictos y mantener el historial limpio.

---

¡Listo! Ahora puedes comenzar a trabajar en tu proyecto. 🛠️
