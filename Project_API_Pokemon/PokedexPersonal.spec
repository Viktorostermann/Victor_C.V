# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_all

datas_streamlit, binaries_streamlit, hiddenimports_streamlit = collect_all('streamlit')

tcl_path = os.path.join(sys.base_prefix, "tcl")

a = Analysis(
    ['launcher/launcher.py'],
    pathex=['C:\\Proyectos\\Project_Manager\\Victor_C.V\\Project_API_Pokemon'],
    datas=[
        # Archivo .env
        ('C:\\Proyectos\\Project_Manager\\Victor_C.V\\Project_API_Pokemon\\.env', '.'),

        # Copia carpetas completas
        ('C:\\Proyectos\\Project_Manager\\Victor_C.V\\Project_API_Pokemon\\app', 'app'),
        ('C:\\Proyectos\\Project_Manager\\Victor_C.V\\Project_API_Pokemon\\assets\\pokemon_images', 'assets/pokemon_images'),
        ('C:\\Proyectos\\Project_Manager\\Victor_C.V\\Project_API_Pokemon\\api', 'api'),
        ('C:\\Proyectos\\Project_Manager\\Victor_C.V\\Project_API_Pokemon\\database', 'database'),
        ('C:\\Proyectos\\Project_Manager\\Victor_C.V\\Project_API_Pokemon\\services', 'services'),

        # Icono Pokéball
        ('C:\\Proyectos\\Project_Manager\\Victor_C.V\\Project_API_Pokemon\\icon.ico', '.'),

        # Tcl/Tk (para Tkinter)
        (os.path.join(tcl_path, "tcl8.6"), "tcl/tcl8.6"),
        (os.path.join(tcl_path, "tk8.6"), "tcl/tk8.6"),
    ] + datas_streamlit,
    hiddenimports=hiddenimports_streamlit,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PokedexPersonal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,   # 🔹 consola visible para ver mensajes de Streamlit
    icon='icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries + binaries_streamlit,
    a.datas,
    strip=False,
    upx=True,
    name='PokedexPersonal',
)
