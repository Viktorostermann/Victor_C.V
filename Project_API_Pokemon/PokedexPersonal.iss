[Setup]
AppName=PokedexPersonal
AppVersion=1.0
DefaultDirName={autopf}\PokedexPersonal
OutputDir=dist\installer
OutputBaseFilename=PokedexPersonalInstaller
Compression=lzma
SolidCompression=yes
SetupIconFile=assets\icon.ico
PrivilegesRequired=lowest
DisableDirPage=yes
DisableProgramGroupPage=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
; Ejecutable principal (onefile)
Source: "dist\PokedexPersonal.exe"; DestDir: "{app}"

; Carpetas raíz necesarias para la app
Source: "dist\app\*"; DestDir: "{app}\app"; Flags: recursesubdirs createallsubdirs
Source: "dist\api\*"; DestDir: "{app}\api"; Flags: recursesubdirs createallsubdirs
Source: "dist\services\*"; DestDir: "{app}\services"; Flags: recursesubdirs createallsubdirs
Source: "dist\assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs createallsubdirs
Source: "dist\database\*"; DestDir: "{app}\database"; Flags: recursesubdirs createallsubdirs
Source: "dist\alembic\*"; DestDir: "{app}\alembic"; Flags: recursesubdirs createallsubdirs


[Icons]
Name: "{userdesktop}\PokedexPersonal"; Filename: "{app}\PokedexPersonal.exe"; WorkingDir: "{app}"
Name: "{group}\PokedexPersonal"; Filename: "{app}\PokedexPersonal.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\PokedexPersonal.exe"; Description: "Ejecutar Pokédex Personal"; \
WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent
