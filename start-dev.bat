@echo off
REM Start OnlyPans development servers

echo 🍳 Starting OnlyPans Development Servers...
echo.

REM Start backend in a new window
echo Starting Django backend server...
start "OnlyPans Backend" cmd /k "cd /d d:\projects\OnlyPans\backend && venv\Scripts\activate && python manage.py runserver"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
echo Starting Next.js frontend server...
start "OnlyPans Frontend" cmd /k "cd /d d:\projects\OnlyPans\frontend && npm run dev"

echo.
echo ✅ Development servers starting...
echo.
echo URLs:
echo - Frontend: http://localhost:3000
echo - Backend API: http://localhost:8000
echo - Django Admin: http://localhost:8000/admin
echo.
echo Press any key to continue...
pause >nul
