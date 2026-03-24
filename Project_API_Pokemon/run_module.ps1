param(
    [string]$ModuleName
)

# Ruta al intérprete de Python de tu entorno virtual
$pythonPath = "C:/Proyectos/Python/.ConquerBlocks/Scripts/python.exe"

# Ejecuta el módulo con -m
& $pythonPath -m $ModuleName
