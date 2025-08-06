#!/usr/bin/env powershell

# OnlyPans Live Data Initialization Test Script

Write-Host "🍳 OnlyPans Live Data Initialization" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

$baseUrl = "https://onlypans.onrender.com"

# Step 1: Wait for backend to be ready
Write-Host "`n⏱️ Waiting for backend deployment..." -ForegroundColor Yellow
do {
    try {
        $healthResponse = Invoke-WebRequest -Uri "$baseUrl/api/health/" -Method GET -TimeoutSec 10
        $isReady = $true
        Write-Host "✅ Backend is ready!" -ForegroundColor Green
    } catch {
        Write-Host "⏳ Backend still deploying... (waiting 10s)" -ForegroundColor Gray
        Start-Sleep -Seconds 10
        $isReady = $false
    }
} while (-not $isReady)

# Step 2: Check current data state
Write-Host "`n📊 Checking current data state..." -ForegroundColor Yellow
try {
    $recipesResponse = Invoke-WebRequest -Uri "$baseUrl/api/recipes/" -Method GET
    $recipes = $recipesResponse.Content | ConvertFrom-Json
    Write-Host "Current recipes: $($recipes.count)" -ForegroundColor Blue
    
    $tagsResponse = Invoke-WebRequest -Uri "$baseUrl/api/recipes/tags/" -Method GET
    $tags = $tagsResponse.Content | ConvertFrom-Json
    Write-Host "Current tags: $($tags.count)" -ForegroundColor Blue
} catch {
    Write-Host "❌ Error checking data: $($_.Exception.Message)" -ForegroundColor Red
}

# Step 3: Instructions for manual initialization
Write-Host "`n🔧 To Initialize Live Data:" -ForegroundColor Cyan
Write-Host "1. Go to Render Dashboard: https://dashboard.render.com/"
Write-Host "2. Select your OnlyPans service"
Write-Host "3. Go to 'Shell' tab"
Write-Host "4. Run the following commands:"
Write-Host ""
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   python manage.py migrate" -ForegroundColor White
Write-Host "   python manage.py create_admin" -ForegroundColor White
Write-Host "   python manage.py init_onlypans" -ForegroundColor White
Write-Host ""
Write-Host "📋 Or run the complete initialization script:" -ForegroundColor Yellow
Write-Host "   python init_production.py" -ForegroundColor White

Write-Host "`n🎯 Expected Results After Initialization:" -ForegroundColor Green
Write-Host "✅ 60+ recipe tags created"
Write-Host "✅ 5 starter recipes with full details"
Write-Host "✅ Admin user: admin / OnlyPans2025!"
Write-Host "✅ Demo user: demo_user / demo123"
Write-Host "✅ Live data in recipes page"

Write-Host "`n📝 Verification Steps:" -ForegroundColor Magenta
Write-Host "1. Check recipes API: $baseUrl/api/recipes/"
Write-Host "2. Check tags API: $baseUrl/api/recipes/tags/"
Write-Host "3. Visit admin panel: $baseUrl/admin/"
Write-Host "4. Check frontend: https://onlypans-ctfazewa7-stanondiekis-projects.vercel.app/recipes"

Write-Host "`n🚀 Your OnlyPans will be fully functional with live data!" -ForegroundColor Green
