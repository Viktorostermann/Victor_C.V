@echo off
REM Script para ejecutar módulos de Python con -m
REM Uso: run_module.bat services.pokemon_service

set PYTHON_PATH=C:\Proyectos\Python\.ConquerBlocks\Scripts\python.exe

if "%~1"=="" (
    echo Debes indicar el módulo a ejecutar. Ejemplo:
    echo run_module.bat services.pokemon_service
    exit /b 1
)

%PYTHON_PATH% -m %1
