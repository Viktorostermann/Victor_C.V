# Ruta del ejecutable
$exePath = "dist\Buscador_Articulo_Texto_Voz\Buscador_Articulo_Texto_Voz.exe"

# Ruta de los recursos de newspaper
$resourcesPath = "newspaper_resources"

# Verificar si el ejecutable existe
if (Test-Path $exePath) {
    Write-Host "✅ Ejecutable encontrado: $exePath"
} else {
    Write-Host "❌ No se encontró el ejecutable. Verifica la ruta."
    exit
}

# Verificar si la carpeta de recursos existe
if (Test-Path $resourcesPath) {
    Write-Host "✅ Carpeta de recursos encontrada: $resourcesPath"
} else {
    Write-Host "⚠️ No se encontró la carpeta de recursos: $resourcesPath"
    Write-Host "Asegúrate de copiar 'newspaper_resources' dentro de la carpeta de ejecución."
}

# Preguntar si quieres lanzar el programa
$launch = Read-Host "¿Deseas ejecutar el programa ahora? (s/n)"
if ($launch -eq "s") {
    Write-Host "🚀 Ejecutando el programa..."
    Start-Process $exePath
} else {
    Write-Host "Script terminado. No se ejecutó el programa."
}