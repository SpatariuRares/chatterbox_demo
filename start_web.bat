@echo off
echo ========================================
echo  Chatterbox TTS Studio - Web Interface
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to create the environment.
    echo.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Gradio application...
echo.
echo Open your browser at: http://localhost:7860
echo Press Ctrl+C to stop the server
echo.
python main-web.py
pause
