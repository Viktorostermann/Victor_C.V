# ⚡ Mini MonkeyType en Python

Aplicación de escritorio desarrollada en Python con `tkinter` que simula una versión simplificada de plataformas como Monkeytype.

Este programa permite medir la velocidad de escritura en tiempo real, evaluar precisión y detectar errores mientras el usuario escribe.

---

## 🚀 Características

* ⚡ Inicio automático al escribir
* 🎯 Evaluación carácter por carácter
* 🟢 Resaltado en verde (correcto)
* 🔴 Resaltado en rojo (errores)
* 📊 Cálculo de WPM (palabras por minuto) en tiempo real
* ⏱️ Medición automática del tiempo
* 🧠 Conteo de errores
* 🔁 Generación de frases aleatorias
* 🖥️ Interfaz limpia y funcional

---

## 🧠 ¿Cómo funciona?

El sistema elimina la necesidad de botones tradicionales:

* El test **comienza automáticamente** al escribir la primera tecla
* Se compara cada carácter en tiempo real
* Se calcula la velocidad constantemente
* Finaliza automáticamente al completar la frase

---

## 🖥️ Interfaz

La aplicación contiene:

* 🔹 **Texto objetivo:** muestra la frase a escribir
* 🔹 **Campo de entrada:** donde el usuario escribe
* 🔹 **Indicador WPM:** velocidad en tiempo real
* 🔹 **Resultado final:** resumen al completar la frase
* 🔹 **Botón "Nueva frase":** reinicia el test

---

## ⚙️ Requisitos

* Python 3.x
* Librerías estándar:

  * `tkinter`
  * `time`
  * `random`

No se requieren dependencias externas.

---

## ▶️ Ejecución

Ejecuta el archivo principal:

```bash
python nombre_del_archivo.py
```

---

## 🎮 Uso

1. Ejecuta la aplicación
2. Observa la frase mostrada
3. Comienza a escribir (el test inicia automáticamente)
4. Corrige errores en tiempo real
5. Al completar la frase, se mostrarán los resultados
6. Presiona **"Nueva frase"** para repetir

---

## 📊 Métricas

* ⚡ **WPM (Words Per Minute):** velocidad de escritura
* ⏱️ **Tiempo total:** duración del test
* ❌ **Errores:** caracteres incorrectos detectados

---

## 🎯 Lógica del sistema

* Se inicia el cronómetro en la primera pulsación
* Se compara cada carácter ingresado con el texto objetivo
* Se recalcula el WPM continuamente
* Se detecta automáticamente el final del test
* Se muestran métricas finales

---

## 🧩 Arquitectura

El programa se basa en:

* Programación orientada a eventos (`tkinter`)
* Captura de teclado en tiempo real
* Renderizado dinámico de texto con etiquetas
* Control de estado del flujo de escritura

---

## ⚠️ Limitaciones actuales

* No guarda historial de resultados
* No calcula precisión porcentual
* No incluye gráficos de rendimiento
* No tiene sistema de niveles o dificultad

---

## 🚀 Mejoras futuras

* 📈 Gráficos de velocidad en tiempo real
* 🧾 Historial de sesiones
* 🎯 Precisión (%) detallada
* 🌐 Exportación de resultados
* 🎨 Interfaz moderna (temas visuales)
* 🧠 Análisis de errores por carácter

---

## 🏁 Conclusión

Este proyecto representa una evolución desde un simple test de escritura hacia una herramienta interactiva en tiempo real, acercándose al comportamiento de aplicaciones modernas.

Ideal para practicar:

* Interfaces gráficas
* Manejo de eventos
* Procesamiento en tiempo real
* Experiencia de usuario (UX)

---

## 👨‍💻 Autor

Desarrollado como ejercicio avanzado de Python, enfocado en lógica interactiva y diseño de herramientas útiles.

Victor Miletic.

---
