@echo off
echo Testing OnlyPans AI Service...
echo.

echo 1. Testing AI Status...
curl -s "https://onlypans.onrender.com/api/ai/status/" 
echo.
echo.

echo 2. AI Status test complete!
echo.
echo If you see "available": true above, your AI service is working.
echo.
echo Next steps:
echo - Login to your frontend with your superuser credentials
echo - Go to AI Assistant page
echo - Try asking a cooking question
echo.
pause
