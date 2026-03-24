[Setup]
AppName=Texto a Voz TkInter v1
AppVersion=1.0
DefaultDirName={pf}\Texto_a_Voz_TkInter_v1
DefaultGroupName=Texto a Voz TkInter v1
OutputBaseFilename=Texto_a_Voz_TkInter_v1_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Buscador_Articulo_Texto_Voz.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Recursos\nouki.png"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Texto a Voz TkInter v1"; Filename: "{app}\Buscador_Articulo_Texto_Voz.exe"
Name: "{commondesktop}\Texto a Voz TkInter v1"; Filename: "{app}\Buscador_Articulo_Texto_Voz.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Opciones adicionales:"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"