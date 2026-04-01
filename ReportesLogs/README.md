
# Dónde guardar la carpeta

Windows:
Puedes colocarla en tu carpeta de proyectos, por ejemplo:
C:\Proyectos\ReportesLogs\

Linux/Mac (Bash):
En tu home o dentro de tu workspace:
/home/usuario/ReportesLogs/

VSCode:
Abre directamente la carpeta ReportesLogs/ como workspace. Así tendrás acceso a todos los scripts y podrás ejecutar el Python desde la terminal integrada.

🔹 Flujo de uso

Capturar logs En CMD:

    .bat: PokedexPersonal.exe > salida.log 2>&1

Capturar logs En Bash:

    .bash: ./PokedexPersonal > salida.log 2>&1

Procesar logs Python:

    bash:  python procesar_logs.py

El script te pedirá:

1- Ruta del archivo log (salida.log)

2- Directorio de salida (reportes/)

3- Formato (md, html, pdf)

4- Resultado: Se generará un archivo en el directorio que elijas con el formato elegido

## 📂 ReportesLogs

Carpeta dedicada a la captura y procesamiento de **logs** de la aplicación `PokedexPersonal`.  
Permite generar reportes en **Markdown (.md)**, **HTML (.html)** y **PDF (.pdf)** con un formato claro y soluciones específicas para cada error o warning detectado.

---

## 📁 Estructura de la carpeta

ReportesLogs/
│
├── procesar_logs.py        # Script principal en Python
├── procesar_logs.bat       # Script Batch para Windows CMD
├── procesar_logs.sh        # Script Bash para Linux/Mac
├── procesar_logs.ps1       # Script PowerShell (opcional)
├── salida.log              # Archivo de logs capturado desde la aplicación
└── reportes/               # Carpeta de salida de reportes
├── reporte.md
├── reporte.html
└── reporte.pdf

## 🚀 Flujo de trabajo

1. **Capturar logs de la aplicación**  
   - En Windows CMD:  

         PokedexPersonal.exe > salida.log 2>&1

   - En Linux/Mac Bash:  

         ./PokedexPersonal > salida.log 2>&1

   - En PowerShell:  

         .\PokedexPersonal.exe *> salida.log

2. **Generar reporte automáticamente**  
   - En Windows:  

         procesar_logs.bat

   - En Linux/Mac:  

         ./procesar_logs.sh

   - En PowerShell:  

         .\procesar_logs.ps1

3. **Formato del reporte**  
   Los scripts llaman al `procesar_logs.py` con parámetros:  
   - `salida.log` → archivo de entrada  
   - `reportes/` → carpeta de salida  
   - `md`, `html` o `pdf` → formato elegido  

   Ejemplo manual:

       python procesar_logs.py salida.log reportes md

📑 Contenido del reporte
Cada registro incluye:

Día

Fecha

Criticidad (Error / Warning)

Por qué falla (descripción clara del problema)

Solución específica (acción concreta para corregirlo)

Árbol jerárquico problema → solución

Ejemplo en Markdown:

### Error: ArrowInvalid

**Día:** Lunes  
**Fecha:** 2026-03-30 11:01:19  
**Criticidad:** Error  
**Por qué falla:** PyArrow intentó convertir texto como 'bulbasaur' a int64.  
**Solución específica:** Convertir columnas mixtas a string con .astype(str).  

Problema → ArrowInvalid  
└── Solución → Convertir columnas mixtas a string

## 📌 Notas importantes

- La carpeta reportes/ se limpia y actualiza cada vez que se genera un nuevo reporte

- Puedes cambiar el formato (md, html, pdf) directamente en los scripts auxiliares

- El script Python también funciona en modo interactivo si no se pasan parámetros
