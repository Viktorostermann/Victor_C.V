Set-Location -Path C:\Proyectos\Python\FastAPI\Project_API_Pokemon

# DIRECTORIOS
$directories = @(
"app",
"app\components",
"api",
"services",
"models",
"config",
"assets",
"tests"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir -Force
}

# ARCHIVOS DEL PROYECTO
$files = @(
"app\streamlit_app.py",
"app\components\pokemon_view.py",
"api\pokeapi_client.py",
"services\pokemon_service.py",
"models\pokemon.py",
"config\settings.py",
"tests\test_pokemon_service.py",
"requirements.txt",
"README.md"
)

foreach ($file in $files) {
    New-Item -ItemType File -Path $file -Force
}

# ARCHIVOS __init__.py PARA MODULOS PYTHON
$modules = @(
"app",
"api",
"services",
"models",
"config"
)

foreach ($module in $modules) {
    New-Item -ItemType File -Path "$module\__init__.py" -Force
}