@echo off
echo Starting Music RPG Attack Game...
python main.py
if errorlevel 1 (
    echo.
    echo Error: Could not run the game.
    echo Make sure Python is installed and pygame is installed.
    echo.
    pause
)
