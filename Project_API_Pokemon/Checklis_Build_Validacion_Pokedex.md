# 🛠️ Checklist de Build y Validación - PokedexPersonal

## 1. Compilación con PyInstaller

- [ ] Ejecutar `Build-Pokedex.ps1`.
- [ ] Confirmar que se genera `dist\PokedexPersonal.exe`.
- [ ] Verificar que se incluyó el icono (`assets\icon.ico`).
- [ ] Asegurar que el build es **onefile** (sin carpeta `_internal`).

## 2. Copiado de carpetas raíz

- [ ] Revisar que en `dist` estén presentes:
  - `app`
  - `api`
  - `services`
  - `assets`
  - `database`
  - `alembic`
  - `launcher`
- [ ] Confirmar que **NO** se copiaron:
  - `.streamlit`
  - `.vscode`
  - `__pycache__`
  - `build`

## 3. Validación con Check-PokedexPaths.ps1

- [ ] Ejecutar `Check-PokedexPaths.ps1`.
- [ ] Confirmar ✔️ en `PokedexPersonal.exe` y carpetas raíz.
- [ ] Confirmar ❌ en carpetas excluidas (`.streamlit`, `.vscode`, etc.).
- [ ] Revisar conteo de archivos en cada carpeta (no deben estar vacías).

## 4. Compilación del instalador con Inno Setup

- [ ] Ejecutar `ISCC.exe PokedexPersonal.iss`.
- [ ] Confirmar que se genera `dist\installer\PokedexPersonalInstaller.exe`.
- [ ] Validar que el instalador:
  - Copia solo las carpetas raíz.
  - Crea acceso directo en escritorio.
  - Lanza el `.exe` al terminar la instalación.

## 5. Firma del ejecutable

- [ ] Confirmar que `Build-Pokedex.ps1` copia `PokedexPersonal.exe` al escritorio como `PokedexPersonalPortable.exe`.
- [ ] Validar que se firma correctamente con `signtool`.
- [ ] Revisar que el ejecutable firmado muestra la firma digital en sus propiedades.

## 6. Prueba de instalación

- [ ] Ejecutar el instalador generado.
- [ ] Confirmar que se instala en `{autopf}\PokedexPersonal`.
- [ ] Abrir el acceso directo en el escritorio.
- [ ] Validar que:
  - El launcher pregunta por el puerto (8051, 8052, 8053, 8080).
  - Se muestra la URL final (`http://localhost:puerto`).
  - Streamlit se levanta en el puerto elegido.
  - La GUI Tkinter permite abrir, copiar URL y salir.

---

✅ Si todos los puntos están marcados, el build y la instalación son correctos y listos para distribución.
