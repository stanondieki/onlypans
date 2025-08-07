@echo off
REM Development setup script for OnlyPans (Windows)

echo 🍳 Setting up OnlyPans for local development...

REM Backend setup
echo 📦 Setting up Python backend...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Go back to root directory
cd ..

REM Frontend setup
echo 🌐 Setting up Node.js frontend...
cd frontend

REM Install Node.js dependencies
echo Installing Node.js dependencies...
npm install

echo ✅ Setup complete!
echo.
echo To start development:
echo 1. Backend: cd backend ^&^& venv\Scripts\activate ^&^& python manage.py runserver
echo 2. Frontend: cd frontend ^&^& npm run dev
echo.
echo URLs:
echo - Frontend: http://localhost:3000
echo - Backend API: http://localhost:8000
echo - Django Admin: http://localhost:8000/admin

pause
