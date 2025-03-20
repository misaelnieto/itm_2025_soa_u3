# Preparar tu Rama de Trabajo para un Pull Request en GitHub 🚀

En este documento, aprenderás los pasos generales para preparar tu rama de trabajo antes de realizar un Pull Request en GitHub. Recuerda que tienes acceso de escritura al repositorio remoto, pero la rama `main` está protegida. Esto significa que no puedes hacer cambios directamente en `main`, y para incorporar tus cambios, debes crear un Pull Request.

## Pasos a seguir 🛠️

1. **Asegúrate de estar en tu rama de trabajo local** 🔍  
   Antes de comenzar, verifica que estás trabajando en tu rama local. Puedes usar el siguiente comando para confirmar:
   ```bash
   git branch
   ```
   Si no estás en tu rama de trabajo, cámbiate a ella con:
   ```bash
   git checkout <nombre-de-tu-rama>
   ```

2. **Actualiza tu rama local con los últimos cambios de `main`** 🔄  
   Es importante que tu rama esté actualizada con los últimos cambios de la rama `main`. Para hacerlo, realiza un rebase:
   ```bash
   git fetch origin
   git rebase origin/main
   ```
   Esto aplicará tus cambios sobre los últimos cambios de `main`, asegurando que no haya conflictos al momento de hacer el Pull Request.

3. **Resuelve conflictos si es necesario** ⚠️  
   Si durante el rebase aparecen conflictos, Git te notificará. Resuelve los conflictos en los archivos afectados, luego añade los cambios resueltos:
   ```bash
   git add <archivo-afectado>
   ```
   Continúa el rebase con:
   ```bash
   git rebase --continue
   ```

4. **Verifica que todo funcione correctamente** ✅  
   Después del rebase, asegúrate de que tu código funcione como esperas. Ejecuta las pruebas necesarias o revisa el comportamiento de tu aplicación.

5. **Sube los cambios a tu rama remota** 📤  
   Una vez que todo esté listo, sube los cambios a tu rama remota. Si realizaste un rebase, es necesario usar el flag `--force-with-lease` para sobrescribir el historial remoto de tu rama:
   ```bash
   git push --force-with-lease
   ```

6. **Crea un Pull Request en GitHub** 📋  
   Ve al repositorio en GitHub y crea un Pull Request desde tu rama hacia la rama `main`. Asegúrate de incluir una descripción clara de los cambios realizados.

## Notas importantes 📝

- **No trabajes directamente en la rama `main`**: Siempre crea una nueva rama para tus cambios.
- **Revisa tu código antes de hacer el Pull Request**: Asegúrate de que tu código esté limpio y cumpla con los estándares del proyecto.
- **Comunica cualquier problema**: Si encuentras dificultades durante el proceso, no dudes en pedir ayuda a tus compañeros o al instructor.

¡Con estos pasos, estarás listo para contribuir al proyecto de manera efectiva! 🎉
