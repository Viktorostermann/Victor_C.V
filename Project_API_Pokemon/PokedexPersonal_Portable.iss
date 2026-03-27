[Setup]
AppName=PokedexPersonalPortable
AppVersion=1.0
DefaultDirName={userdesktop}\PokedexPersonalPortable
OutputDir=dist\portable
OutputBaseFilename=PokedexPersonalPortable
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Proyectos\Project_Manager\Victor_C.V\Project_API_Pokemon\icon.ico

[Files]
; Copia el ejecutable portable ya generado con PyInstaller
Source: "C:\Proyectos\Project_Manager\Victor_C.V\Project_API_Pokemon\dist\PokedexPersonal\PokedexPersonal.exe"; DestDir: "{app}"; Flags: ignoreversion
; Copia recursos adicionales si tu app los necesita
Source: "C:\Proyectos\Project_Manager\Victor_C.V\Project_API_Pokemon\dist\PokedexPersonal\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Run]
; Ejecuta directamente el portable después de extraerlo
Filename: "{app}\PokedexPersonal.exe"; Flags: nowait postinstall skipifsilent
