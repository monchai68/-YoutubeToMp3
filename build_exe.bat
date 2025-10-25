@echo off
echo Building YouTube to MP3/MP4 Converter with Playlist Support...
echo This may take a few minutes...
echo.

cd /d "%~dp0"

echo Installing PyInstaller...
D:\code\python\YoutubeToMp3\.venv\Scripts\pip.exe install pyinstaller

echo.
echo Building EXE file...
D:\code\python\YoutubeToMp3\.venv\Scripts\pyinstaller.exe --onefile --windowed --name "YouTube_to_MP3_Converter_Playlist" youtubeToMp3.py

echo.
echo Build completed!
echo EXE file location: dist\YouTube_to_MP3_Converter_Playlist.exe
echo.
pause