Write-Host "Desinstalando Texto a Voz TkInter v1..." -ForegroundColor Cyan

# Carpeta de datos del usuario (donde guardamos audios y logs)
$AppDataPath = Join-Path $env:APPDATA "Texto_a_Voz_TkInter_v1"

# Acceso directo del menú inicio
$StartMenu = [Environment]::GetFolderPath("Programs")
$Shortcut = Join-Path $StartMenu "Texto a Voz TkInter v1.lnk"

# Eliminar datos
if (Test-Path $AppDataPath) {
    Remove-Item $AppDataPath -Recurse -Force
    Write-Host "Carpeta eliminada: $AppDataPath" -ForegroundColor Green
} else {
    Write-Host "No se encontró carpeta de datos." -ForegroundColor Yellow
}

# Eliminar acceso directo
if (Test-Path $Shortcut) {
    Remove-Item $Shortcut -Force
    Write-Host "Acceso directo eliminado." -ForegroundColor Green
} else {
    Write-Host "Acceso directo no encontrado." -ForegroundColor Yellow
}

Write-Host "Desinstalación completada." -ForegroundColor Cyan
Pause