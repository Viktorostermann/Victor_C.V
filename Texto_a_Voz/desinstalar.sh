#!/bin/bash

echo "🧹 Desinstalando Texto a Voz TkInter v1..."

# Ruta de instalación
DEST="$HOME/.texto_voz_tkinter_v1"
DESKTOP_FILE="$HOME/.local/share/applications/Texto_a_Voz_TkInter_v1.desktop"

# Eliminar archivos y carpetas
rm -rf "$DEST"
echo "🗑️ Carpeta eliminada: $DEST"

# Eliminar lanzador
if [ -f "$DESKTOP_FILE" ]; then
    rm "$DESKTOP_FILE"
    echo "🗑️ Lanzador eliminado: $DESKTOP_FILE"
else
    echo "⚠️ Lanzador no encontrado en: $DESKTOP_FILE"
fi

# Actualizar menú (opcional)
update-desktop-database ~/.local/share/applications/ 2>/dev/null

echo "✅ Desinstalación completada."
