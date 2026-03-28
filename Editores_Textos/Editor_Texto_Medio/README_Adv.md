# 🧠 Mini IDE Pro en Python

Editor de código avanzado desarrollado en Python con `tkinter`, inspirado en entornos modernos como Visual Studio Code y PyCharm.

Este proyecto implementa múltiples funcionalidades clave de un IDE real, incluyendo ejecución de código, pestañas, consola integrada y exportación a PDF.

---

## 🚀 Características

* 📑 **Pestañas múltiples** (`ttk.Notebook`)
* 🖥️ **Consola integrada** para salida de ejecución
* ▶️ **Ejecución de código Python**
* 📄 **Exportación a PDF**
* 🎨 **Interfaz estilo dark mode**
* 🧰 **Toolbar con botones grandes y visibles**
* 📝 Editor de texto multilínea adaptable

---

## 🧠 ¿Qué hace este IDE?

Permite:

* Escribir código en múltiples archivos simultáneamente
* Ejecutar scripts Python directamente desde la interfaz
* Visualizar resultados y errores en una consola integrada
* Exportar el código a formato PDF
* Gestionar múltiples sesiones mediante pestañas

---

## 🖥️ Interfaz

La aplicación se divide en:

* 🔹 **Toolbar superior:** acciones principales (Nueva pestaña, Ejecutar, Exportar)
* 🔹 **Área central:** editor con pestañas
* 🔹 **Panel inferior:** consola de salida
* 🔹 **Menú superior:** opciones adicionales

---

## ⚙️ Requisitos

* Python 3.x
* Librerías necesarias:

  * `tkinter`
  * `subprocess`
  * `tempfile`
  * `reportlab`

Instalar `reportlab` si no lo tienes:

```bash id="cmd002"
pip install reportlab
```

---

## ▶️ Ejecución

```bash id="cmd003"
python nombre_del_archivo.py
```

---

## 🎮 Uso

* 📄 **Nueva pestaña:** crea un nuevo archivo
* ▶️ **Ejecutar:** corre el código Python actual
* 📄 **Exportar PDF:** guarda el contenido como documento
* 🖥️ **Consola:** muestra resultados y errores

---

## 📊 Funcionalidades técnicas

### Ejecución de código

El código se ejecuta mediante archivos temporales usando `subprocess`.

### Consola integrada

Captura:

* salida estándar (`stdout`)
* errores (`stderr`)

### Exportación a PDF

Convierte el código en un documento estructurado usando `reportlab`.

### Sistema de pestañas

Permite trabajar con múltiples documentos simultáneamente.

---

## ⚠️ Limitaciones actuales

* No tiene resaltado de sintaxis
* No incluye autocompletado
* No guarda archivos directamente desde pestañas
* No tiene explorador de archivos lateral

---

## 🚀 Mejoras futuras

* 🎨 Resaltado de sintaxis (Python)
* 🧠 Autocompletado inteligente
* 📂 Explorador de archivos lateral
* 💾 Guardado/abrir archivos por pestaña
* 🖥️ Consola interactiva (`input()`)
* 🔄 Redimensionamiento dinámico de paneles

---

## 🏁 Conclusión

Este proyecto representa un paso importante hacia la construcción de un IDE funcional desde cero, integrando:

* Interfaces gráficas
* Ejecución de código
* Gestión de múltiples documentos
* Exportación de contenido

Una base sólida para evolucionar hacia herramientas de desarrollo más complejas.

---

## 👨‍💻 Autor

**Victor Miletic**

---
