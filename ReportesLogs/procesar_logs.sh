#!/bin/bash
# ============================================
# Script para capturar logs y generar reporte
# ============================================

# 1. Ejecuta tu aplicación y guarda salida en salida.log
./PokedexPersonal > salida.log 2>&1

# 2. Llama al script Python para procesar los logs
#    Parámetros: archivo log, directorio de salida, formato
python3 procesar_logs.py salida.log reportes md

# Puedes cambiar "md" por "html" o "pdf" según el formato deseado

# 🔹 Cómo funciona

# Ejecutas tu programa desde cualquiera de las consolas (CMD, PowerShell, Bash).

# La salida se guarda en salida.log.

# Llamas al script Python (procesar_logs.py).

# El script analiza el log, genera un árbol problema → solución, y exporta Markdown, HTML y PDF en el directorio que elijas.

# Cada registro tiene encabezado: Día, Fecha, Criticidad, Por qué falla, Solución, y dos saltos de línea entre registros.

# ✅ Con esto tienes un flujo global que funciona en todas las consolas.