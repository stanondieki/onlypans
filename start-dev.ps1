# OnlyPans Development Startup Script
Write-Host "🍳 Starting OnlyPans Development Servers..." -ForegroundColor Green
Write-Host ""

# Start backend server
Write-Host "Starting Django backend server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'd:\projects\OnlyPans\backend'; & 'C:/Program Files/Python312/python.exe' manage.py runserver"

# Wait a moment
Start-Sleep -Seconds 3

# Start frontend server
Write-Host "Starting Next.js frontend server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'd:\projects\OnlyPans\frontend'; npm run dev"

Write-Host ""
Write-Host "✅ Development servers starting..." -ForegroundColor Green
Write-Host ""
Write-Host "URLs:" -ForegroundColor Cyan
Write-Host "- Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "- Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "- Django Admin: http://localhost:8000/admin" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
