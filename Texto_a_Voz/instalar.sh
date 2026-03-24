#!/bin/bash

echo "🔧 Instalando Texto a Voz TkInter v1..."

# Ruta base del paquete
BASE=$(pwd)

# Crear carpeta de instalación local
DEST="$HOME/.texto_voz_tkinter_v1"
mkdir -p "$DEST"

# Copiar ejecutable y recursos
cp -r "$BASE/dist" "$DEST/"
cp -r "$BASE/Recursos" "$DEST/"
cp -r "$BASE/Reportes" "$DEST/"

# Copiar lanzador .desktop
DESKTOP_FILE="$HOME/.local/share/applications/Texto_a_Voz_TkInter_v1.desktop"
cp "$BASE/Texto_a_Voz_TkInter_v1.desktop" "$DESKTOP_FILE"

# Ajustar rutas en el .desktop
sed -i "s|Exec=.*|Exec=$DEST/dist/Texto_a_Voz_TkInter_v1|g" "$DESKTOP_FILE"
sed -i "s|Icon=.*|Icon=$DEST/Recursos/nouki.png|g" "$DESKTOP_FILE"

# Dar permisos
chmod +x "$DEST/dist/Texto_a_Voz_TkInter_v1"
chmod +x "$DESKTOP_FILE"

# 🔽 Instalar ícono en ruta estándar del sistema
echo "🖼️ Instalando ícono en /usr/share/icons/hicolor..."
sudo install -Dm644 "$BASE/Recursos/nouki.png" /usr/share/icons/hicolor/256x256/apps/viktoreapp.png
sudo update-icon-caches /usr/share/icons/hicolor || true

# 🔽 Mensaje final
echo "✅ Instalación completada."
echo "📂 Ejecutable instalado en: $DEST/dist/Texto_a_Voz_TkInter_v1"
echo "🖼️ Ícono configurado localmente: $DEST/Recursos/nouki.png"
echo "🖼️ Ícono instalado globalmente como: viktoreapp.png"
echo "🚀 Puedes abrir la app desde el menú de aplicaciones."
