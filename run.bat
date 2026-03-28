@echo off
echo.
echo  ██████╗ ███████╗██████╗ ███╗   ███╗ █████╗ ██╗
echo  ██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔══██╗██║
echo  ██║  ██║█████╗  ██████╔╝██╔████╔██║███████║██║
echo  ██║  ██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══██║██║
echo  ██████╔╝███████╗██║  ██║██║ ╚═╝ ██║██║  ██║██║
echo  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝
echo.
echo  AI Skin Disease Detection System
echo ═══════════════════════════════════════
echo.

echo [1/3] Installing dependencies...
pip install -r requirements.txt
echo.

echo [2/3] Starting DermAI server...
echo.
echo  Open your browser at: http://localhost:5000
echo  Press Ctrl+C to stop the server
echo.

echo [3/3] Launching browser...
start "" "http://localhost:5000"

python app.py
pause
