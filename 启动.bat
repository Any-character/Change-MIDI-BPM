@echo off
cd /d "%~dp0"

echo MIDI BPM Tool is starting...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [Error] Python not found, please install Python 3.x first.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

python -c "import mido" >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing mido library...
    pip install mido
    if %errorlevel% neq 0 (
        echo [Error] Failed to install mido.
        pause
        exit /b 1
    )
)

python change_midi_bpm_gui.py
if %errorlevel% neq 0 (
    echo.
    echo [Error] Program exited with code: %errorlevel%
    pause
    exit /b 1
)
