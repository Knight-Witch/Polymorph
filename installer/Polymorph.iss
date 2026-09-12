#define MyAppName "Polymorph"
#define MyAppVersion "0.1.0-dev.16"
#define MyAppPublisher "Knight Witch"
#define MyAppURL "https://github.com/Knight-Witch/Polymorph"
#define MyAppExeName "Polymorph.exe"

[Setup]
AppId={{34DA7F8D-55E7-4E54-B83C-1CA38E381B76}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
DefaultDirName={localappdata}\Programs\Polymorph
DefaultGroupName=Polymorph
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=Polymorph_Setup_v{#MyAppVersion}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
SetupIconFile=..\build\polymorph_placeholder.ico
UninstallDisplayIcon={app}\Polymorph.exe
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "..\dist\Polymorph\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Polymorph"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Polymorph"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Polymorph"; Flags: nowait postinstall skipifsilent
