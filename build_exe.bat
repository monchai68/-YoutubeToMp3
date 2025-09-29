@echo off
echo Building YouTube to MP3 Converter as EXE file...
echo This may take a few minutes...
echo.

cd /d "%~dp0"

echo Installing PyInstaller...
D:\code\python\YoutubeToMp3\.venv\Scripts\pip.exe install pyinstaller

echo.
echo Building EXE file...
D:\code\python\YoutubeToMp3\.venv\Scripts\pyinstaller.exe --onefile --windowed --name "YouTube_to_MP3_Converter" youtubeToMp3_V2.py

echo.
echo Build completed!
echo EXE file location: dist\YouTube_to_MP3_Converter.exe
echo.
pause