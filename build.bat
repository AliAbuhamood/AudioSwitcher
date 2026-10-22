@echo off
cd /d "%~dp0"

if not exist SoundVolumeView.exe (
    echo ERROR: SoundVolumeView.exe is missing from this folder.
    echo Download soundvolumeview-x64.zip from nirsoft.net, extract SoundVolumeView.exe here, then run this again.
    pause
    exit /b
)

echo Installing PyInstaller...
python -m pip install pyinstaller
echo.
echo Building AudioSwitcher.exe ...
if exist icon.ico (
    python -m PyInstaller --onefile --noconsole --name AudioSwitcher --icon icon.ico --add-data "icon.ico;." --add-data "SoundVolumeView.exe;." AudioSwitcher.pyw
) else (
    python -m PyInstaller --onefile --noconsole --name AudioSwitcher --add-data "SoundVolumeView.exe;." AudioSwitcher.pyw
)
echo.
echo Done! Your program is in the "dist" folder: dist\AudioSwitcher.exe
pause
