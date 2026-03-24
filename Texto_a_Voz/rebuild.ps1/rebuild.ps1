Write-Host "=== REBUILD AUTOMATICO ===" -ForegroundColor Cyan

$project = "C:\Proyectos\Python\Proyectos\Texto_a_Voz"
$sitepkg = "C:\Proyectos\Python\.ConquerBlocks\Lib\site-packages\newspaper\resources"
$localResources = "$project\newspaper_resources"

Set-Location $project

Write-Host "Limpiando..."
Remove-Item build -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item dist -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item __pycache__ -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $localResources -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Copiando recursos newspaper..."
New-Item -ItemType Directory -Path $localResources | Out-Null
Copy-Item $sitepkg "$localResources\resources" -Recurse -Force

Write-Host "Compilando..."
pyinstaller --clean Buscador_Articulo_Texto_Voz.spec

Write-Host "=== TERMINADO ===" -ForegroundColor Green