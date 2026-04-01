📦 PokedexPersonal

Aplicación de escritorio basada en Streamlit + Python, empaquetada como ejecutable (.exe) y distribuible mediante instalador.

Permite visualizar Pokémon de la primera generación consumiendo la PokéAPI, con una interfaz sencilla y funcional.

🚀 Características
🔍 Visualización de Pokémon (nombre e imagen)
⏭ Navegación entre Pokémon (Anterior / Siguiente)
🌐 Consumo de datos desde PokéAPI
🖥 Interfaz de escritorio con Tkinter
⚙️ Servidor Streamlit integrado automáticamente
📦 Distribución mediante instalador (.exe)
🧱 Arquitectura del proyecto

Estructura modular orientada a buenas prácticas:

project/
│
├── app/                # Interfaz Streamlit
├── api/                # Consumo de API externa
├── services/           # Lógica de negocio
├── database/           # Manejo de datos
├── assets/             # Imágenes (Pokémon)
├── launcher/           # Lanzador de la app (Tkinter + Streamlit)
├── .env                # Variables de entorno
└── main.spec           # Configuración PyInstaller

⚙️ Instalación (modo desarrollo)

1. Clonar repositorio
git clone https://github.com/usuario/Api_PokeAPI.git
cd Api_PokeAPI

2. Crear entorno virtual
python -m venv .venv
source .venv/Scripts/activate  # Windows

3. Instalar dependencias
pip install -r requirements.txt
▶️ Ejecución en desarrollo
streamlit run app/app.py
🖥 Ejecución como aplicación (usuario final)

Después de compilar:

👉 Ejecutar:

PokedexPersonalSetup.exe

Esto:

Instala la aplicación
Crea accesos directos
Permite ejecutar sin Python instalado

🛠 Empaquetado

🔹 Generar ejecutable (PyInstaller)
pyinstaller main.spec

Salida:

dist/PokedexPersonal/
🔹 Crear instalador (Inno Setup)

Compilar el archivo .iss:

Resultado:

dist/installer/PokedexPersonalSetup.exe
⚠️ Notas importantes
La aplicación NO requiere Python instalado en el equipo final
Streamlit se ejecuta internamente usando el ejecutable empaquetado
No se utilizan rutas absolutas (compatible con cualquier entorno)
Compatible con Windows
🧠 Consideraciones técnicas
Uso de sys._MEIPASS para acceso a recursos empaquetados
Uso de sys.executable para ejecutar Streamlit dentro del .exe
Separación de capas:
UI
lógica
datos

🔧 Comandos útiles

# Verificar base de datos
python -m database.check_db
🧪 Recomendaciones
Probar el instalador en una máquina limpia (o VM)
Evitar dependencias externas no empaquetadas
Mantener rutas relativas siempre
👨‍💻 Autor

Victor Miletic

📄 Licencia

MIT License

⚡ Nota final

Este proyecto ya no es solo un script:

es una aplicación distribuible lista para usuarios finales.