# AudioSwitcher
A small Windows tool that lists every app playing audio and lets you drag each app between your headphones and your speakers. Example: game on headphones, Discord on speakers.

Features
Compact window with two columns: 🎧 Headphones and 🔊 Speaker
Drag an app from one column to the other and its audio moves instantly
Pick your devices once, it remembers them
No installation, a single exe
Download & use
Go to Releases and download AudioSwitcher.exe.
Run it.
Choose your headphones and speaker at the top.
Drag apps between the columns.

An app only shows up while it is playing audio.

Notes
Windows SmartScreen may warn you because the exe is unsigned. Click More info → Run anyway.
Some antivirus tools falsely flag PyInstaller executables. The source is open so you can review it.
Discord: set its Output Device to Default and restart it after changing the device.
The tool does not modify or inject into any game or app. It only changes the output device per app, like the Windows Volume Mixer. Still, use it at your own risk with games that have anti-cheat.
Build from source
Install Python (check Add Python to PATH).
Download SoundVolumeView (x64) from nirsoft.net and put SoundVolumeView.exe in the same folder.
Run build.bat. The result is dist\AudioSwitcher.exe.
Credits

Relies on SoundVolumeView by NirSoft to set the audio device per app. That tool is not mine and belongs to its author.
