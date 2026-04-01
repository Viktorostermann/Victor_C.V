# 🧠 Test de Velocidad de Escritura en Python

Aplicación de escritorio desarrollada en Python utilizando `tkinter` para medir la velocidad y precisión de escritura del usuario.

Este programa permite evaluar no solo el tiempo total de escritura, sino también métricas avanzadas como correcciones, pausas y tiempo efectivo de escritura.

---

## 🚀 Características

* ✅ Interfaz gráfica intuitiva (GUI)
* ✅ Generación aleatoria de frases
* ✅ Medición de tiempo total de escritura
* ✅ Conteo de correcciones (uso de Backspace)
* ✅ Detección de pausas durante la escritura
* ✅ Cálculo de tiempo efectivo (sin pausas)
* ✅ Navegación con teclado (Enter y Tab)
* ✅ Botón de reinicio completo (Limpiar)
* ✅ Tabla tipo DataFrame para reporte de métricas

---

## 🖥️ Interfaz

La aplicación está dividida en secciones:

* 🔹 **Zona superior:** instrucciones y frase a escribir
* 🔹 **Zona central:** campo de texto expandible
* 🔹 **Zona de control:** botones (Iniciar, Finalizar, Limpiar)
* 🔹 **Zona inferior:** tabla de resultados y métricas

---

## ⚙️ Requisitos

* Python 3.x
* Librerías estándar:

  * `tkinter`
  * `time`
  * `random`

(No se requieren instalaciones adicionales)

---

## ▶️ Ejecución

1. Clona o descarga el proyecto
2. Ejecuta el archivo:

```bash
python nombre_del_archivo.py
```

---

## 🎮 Uso

1. Presiona **Iniciar**
2. Escribe la frase mostrada
3. Presiona **Finalizar** o usa `Tab + Enter`
4. Observa tus métricas en la tabla
5. Usa **Limpiar** para reiniciar el test

---

## 📊 Métricas registradas

* ⏱️ **Tiempo total:** duración completa del test
* ⌫ **Correcciones:** número de veces que se usó Backspace
* ⏸️ **Tiempo en pausas:** tiempo sin actividad (>1.5s)
* ⚡ **Tiempo efectivo:** tiempo real escribiendo (sin pausas)

---

## 🧠 Lógica del sistema

* Se inicia un cronómetro al presionar **Iniciar**
* Se captura cada tecla presionada
* Se detectan pausas automáticamente
* Se validan errores comparando texto final con la frase original
* Se generan métricas en tiempo real

---

## ⌨️ Controles de teclado

* `Enter` → Ejecuta botones
* `Tab` → Cambia el foco (no inserta espacios)
* `Backspace` → Cuenta como corrección

---

## ⚠️ Notas importantes

* El botón **Finalizar** debería iniciar desactivado para evitar errores de flujo
* En la función `limpiar()`, se recomienda:

```python
btn_finalizar.config(state=DISABLED)
```

* Esto evita estados inconsistentes en la aplicación

---

## 📌 Mejoras futuras

* 📈 Cálculo de palabras por minuto (WPM)
* 🧾 Historial de sesiones
* 🎯 Resaltado de errores en tiempo real
* 🌐 Exportación de resultados
* 🎨 Mejora visual (estilos modernos)

---

## 🏁 Conclusión

Este proyecto no solo mide velocidad de escritura, sino que introduce conceptos clave de desarrollo:

* Gestión de estado
* Eventos de teclado
* Interfaces adaptables
* Telemetría básica

Una base sólida para evolucionar hacia herramientas más avanzadas.

---

## 👨‍💻 Autor

Proyecto desarrollado como práctica avanzada de Python + GUI + lógica de interacción.

Victor Miletic.

---
