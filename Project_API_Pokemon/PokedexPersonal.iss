[Setup]
AppName=PokedexPersonal
AppVersion=1.0
DefaultDirName={pf}\PokedexPersonal
DefaultGroupName=PokedexPersonal
UninstallDisplayIcon={app}\PokedexPersonal.exe
OutputDir=dist\installer
OutputBaseFilename=PokedexPersonalSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Proyectos\Project_Manager\Victor_C.V\Project_API_Pokemon\icon.ico

[Files]
Source: "C:\Proyectos\Project_Manager\Victor_C.V\Project_API_Pokemon\dist\PokedexPersonal\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Proyectos\Project_Manager\Victor_C.V\Project_API_Pokemon\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\PokedexPersonal"; Filename: "{app}\PokedexPersonal.exe"; IconFilename: "{app}\icon.ico"
Name: "{commondesktop}\PokedexPersonal"; Filename: "{app}\PokedexPersonal.exe"; IconFilename: "{app}\icon.ico"

[Run]
Filename: "{app}\PokedexPersonal.exe"; Flags: nowait postinstall skipifsilent
