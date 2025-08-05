#!/usr/bin/env powershell

# OnlyPans API Testing Script
# This script tests all the main API endpoints

$baseUrl = "https://onlypans.onrender.com"

Write-Host "🧪 OnlyPans API Testing Script" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Test 1: Health Check
Write-Host "`n1. Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-WebRequest -Uri "$baseUrl/api/health/" -Method GET
    Write-Host "✅ Health Check: $($healthResponse.Content)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health Check Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: User Registration
Write-Host "`n2. Testing User Registration..." -ForegroundColor Yellow
$testUser = @{
    username = "testuser$(Get-Random -Minimum 100 -Maximum 999)"
    email = "test$(Get-Random -Minimum 100 -Maximum 999)@example.com"
    password = "testpass123"
    password_confirm = "testpass123"
    first_name = "Test"
    last_name = "User"
} | ConvertTo-Json

try {
    $regResponse = Invoke-WebRequest -Uri "$baseUrl/api/auth/register/" -Method POST -Body $testUser -ContentType "application/json"
    Write-Host "✅ User Registration: Success" -ForegroundColor Green
    $userData = $regResponse.Content | ConvertFrom-Json
    $username = $userData.user.username
} catch {
    if ($_.Exception.Response.StatusCode -eq 400) {
        Write-Host "⚠️ User Registration: User might already exist, trying login..." -ForegroundColor Yellow
        $username = "testuser123"  # Use existing user
    } else {
        Write-Host "❌ User Registration Failed: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# Test 3: User Login
Write-Host "`n3. Testing User Login..." -ForegroundColor Yellow
$loginData = @{
    username = $username
    password = "testpass123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-WebRequest -Uri "$baseUrl/api/auth/login/" -Method POST -Body $loginData -ContentType "application/json"
    Write-Host "✅ User Login: Success" -ForegroundColor Green
    $loginResult = $loginResponse.Content | ConvertFrom-Json
    $token = $loginResult.access
    
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
} catch {
    Write-Host "❌ User Login Failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 4: User Profile
Write-Host "`n4. Testing User Profile..." -ForegroundColor Yellow
try {
    $profileResponse = Invoke-WebRequest -Uri "$baseUrl/api/auth/profile/" -Method GET -Headers $headers
    Write-Host "✅ User Profile: Success" -ForegroundColor Green
} catch {
    Write-Host "❌ User Profile Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Recipes List
Write-Host "`n5. Testing Recipes List..." -ForegroundColor Yellow
try {
    $recipesResponse = Invoke-WebRequest -Uri "$baseUrl/api/recipes/" -Method GET
    $recipes = $recipesResponse.Content | ConvertFrom-Json
    Write-Host "✅ Recipes List: Found $($recipes.count) recipes" -ForegroundColor Green
} catch {
    Write-Host "❌ Recipes List Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 6: Recipe Tags
Write-Host "`n6. Testing Recipe Tags..." -ForegroundColor Yellow
try {
    $tagsResponse = Invoke-WebRequest -Uri "$baseUrl/api/recipes/tags/" -Method GET
    $tags = $tagsResponse.Content | ConvertFrom-Json
    Write-Host "✅ Recipe Tags: Found $($tags.count) tags" -ForegroundColor Green
} catch {
    Write-Host "❌ Recipe Tags Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 7: Meal Plans
Write-Host "`n7. Testing Meal Plans..." -ForegroundColor Yellow
try {
    $mealPlansResponse = Invoke-WebRequest -Uri "$baseUrl/api/meals/plans/" -Method GET -Headers $headers
    $mealPlans = $mealPlansResponse.Content | ConvertFrom-Json
    Write-Host "✅ Meal Plans: Found $($mealPlans.count) meal plans" -ForegroundColor Green
} catch {
    Write-Host "❌ Meal Plans Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 8: User Statistics
Write-Host "`n8. Testing User Statistics..." -ForegroundColor Yellow
try {
    $statsResponse = Invoke-WebRequest -Uri "$baseUrl/api/auth/stats/" -Method GET -Headers $headers
    Write-Host "✅ User Statistics: Success" -ForegroundColor Green
} catch {
    Write-Host "❌ User Statistics Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 9: User Dashboard
Write-Host "`n9. Testing User Dashboard..." -ForegroundColor Yellow
try {
    $dashboardResponse = Invoke-WebRequest -Uri "$baseUrl/api/auth/dashboard/" -Method GET -Headers $headers
    Write-Host "✅ User Dashboard: Success" -ForegroundColor Green
} catch {
    Write-Host "❌ User Dashboard Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 API Testing Complete!" -ForegroundColor Green
Write-Host "Your OnlyPans backend is running at: $baseUrl" -ForegroundColor Cyan
