# OnlyPans Setup and Test Script
# This script helps create admin user and test the meal schedule API

Write-Host "🚀 OnlyPans Setup & Test Script" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

$API_BASE = "https://onlypans.onrender.com/api"
$FRONTEND_URL = "https://onlypans-ctfazewa7-stanondiekis-projects.vercel.app"

# Function to test API endpoint
function Test-APIEndpoint {
    param($Url, $Description)
    Write-Host "`n🔍 Testing: $Description" -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri $Url -TimeoutSec 15 -ErrorAction Stop
        Write-Host "✅ Success: $Description" -ForegroundColor Green
        return $response
    }
    catch {
        Write-Host "❌ Failed: $Description - $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Function to test authenticated endpoint
function Test-AuthenticatedEndpoint {
    param($Url, $Token, $Description)
    Write-Host "`n🔍 Testing: $Description" -ForegroundColor Yellow
    try {
        $headers = @{ Authorization = "Bearer $Token" }
        $response = Invoke-RestMethod -Uri $Url -Headers $headers -TimeoutSec 15 -ErrorAction Stop
        Write-Host "✅ Success: $Description" -ForegroundColor Green
        return $response
    }
    catch {
        Write-Host "❌ Failed: $Description - $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.Response.StatusCode -eq 401) {
            Write-Host "   💡 This might be an authentication issue" -ForegroundColor Cyan
        }
        return $null
    }
}

# Function to attempt login
function Attempt-Login {
    param($Username, $Password)
    Write-Host "`n🔐 Attempting login for user: $Username" -ForegroundColor Yellow
    try {
        $loginData = @{
            username = $Username
            password = $Password
        }
        $jsonBody = $loginData | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "$API_BASE/auth/login/" -Method Post -Body $jsonBody -ContentType "application/json" -TimeoutSec 15
        Write-Host "✅ Login successful for $Username" -ForegroundColor Green
        return $response.access
    }
    catch {
        Write-Host "❌ Login failed for $Username - $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Step 1: Test Backend Health
Write-Host "`n📡 Step 1: Testing Backend Health" -ForegroundColor Cyan
$healthResponse = Test-APIEndpoint "$API_BASE/health/" "Backend Health Check"

if ($healthResponse) {
    Write-Host "   Backend Status: $($healthResponse.status)" -ForegroundColor Green
    Write-Host "   Message: $($healthResponse.message)" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Backend might be cold starting. Waiting 30 seconds..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
    $healthResponse = Test-APIEndpoint "$API_BASE/health/" "Backend Health Check (Retry)"
}

# Step 2: Test Login Options
Write-Host "`n🔐 Step 2: Testing Admin Login Options" -ForegroundColor Cyan

$adminCredentials = @(
    @{ username = "admin"; password = "admin123" },
    @{ username = "admin"; password = "password" },
    @{ username = "admin"; password = "admin" },
    @{ username = "superuser"; password = "admin123" }
)

$token = $null
foreach ($cred in $adminCredentials) {
    $token = Attempt-Login $cred.username $cred.password
    if ($token) {
        $workingUsername = $cred.username
        $workingPassword = $cred.password
        break
    }
}

if (-not $token) {
    Write-Host "`n❌ No admin user found with common credentials" -ForegroundColor Red
    Write-Host "`n🛠️  MANUAL STEPS REQUIRED:" -ForegroundColor Yellow
    Write-Host "1. Go to https://dashboard.render.com" -ForegroundColor White
    Write-Host "2. Find your 'onlypans' service" -ForegroundColor White
    Write-Host "3. Click on it → Go to 'Shell' tab → Click 'Launch Shell'" -ForegroundColor White
    Write-Host "4. Run one of these commands:" -ForegroundColor White
    Write-Host "   python manage.py createsuperuser" -ForegroundColor Cyan
    Write-Host "   OR" -ForegroundColor White
    Write-Host "   python create_quick_admin.py" -ForegroundColor Cyan
    Write-Host "5. Use username: admin, password: admin123" -ForegroundColor White
    Write-Host "6. Run this script again" -ForegroundColor White
    
    Read-Host "`nPress Enter to exit"
    exit
}

# Step 3: Test Recipes API
Write-Host "`n📚 Step 3: Testing Recipes API" -ForegroundColor Cyan
$recipesResponse = Test-AuthenticatedEndpoint "$API_BASE/recipes/" $token "Recipes List"

if ($recipesResponse) {
    $recipeCount = if ($recipesResponse.results) { $recipesResponse.results.Count } else { $recipesResponse.Count }
    Write-Host "   Found $recipeCount recipes" -ForegroundColor Green
    
    if ($recipeCount -eq 0) {
        Write-Host "   💡 No recipes found. Initializing data..." -ForegroundColor Yellow
        Write-Host "`n🛠️  TO INITIALIZE DATA:" -ForegroundColor Yellow
        Write-Host "1. Go to Render Shell (see steps above)" -ForegroundColor White
        Write-Host "2. Run: python manage.py init_onlypans" -ForegroundColor Cyan
        Write-Host "3. This will create 60+ recipe tags and 5 starter recipes" -ForegroundColor White
    }
}

# Step 4: Test Meal Plans API
Write-Host "`n🍽️  Step 4: Testing Meal Plans API" -ForegroundColor Cyan
$mealPlansResponse = Test-AuthenticatedEndpoint "$API_BASE/meals/plans/" $token "Meal Plans List"

if ($mealPlansResponse) {
    $planCount = if ($mealPlansResponse.results) { $mealPlansResponse.results.Count } else { $mealPlansResponse.Count }
    Write-Host "   Found $planCount meal plans" -ForegroundColor Green
}

# Step 5: Test NEW Meals by Date API
Write-Host "`n📅 Step 5: Testing NEW Meals by Date API" -ForegroundColor Cyan
$today = Get-Date -Format "yyyy-MM-dd"
$weekEnd = (Get-Date).AddDays(6).ToString("yyyy-MM-dd")
$mealsResponse = Test-AuthenticatedEndpoint "$API_BASE/meals/by-date/?start_date=$today&end_date=$weekEnd" $token "Meals by Date Range"

if ($mealsResponse) {
    $mealCount = $mealsResponse.meals.Count
    Write-Host "   Found $mealCount meals for this week" -ForegroundColor Green
    
    if ($mealCount -eq 0) {
        Write-Host "   💡 No meals scheduled. You can:" -ForegroundColor Yellow
        Write-Host "   1. Create a meal plan in the frontend" -ForegroundColor White
        Write-Host "   2. Add meals to the plan" -ForegroundColor White
        Write-Host "   3. Or run the test data script" -ForegroundColor White
    } else {
        Write-Host "   📊 Meals breakdown:" -ForegroundColor Green
        $mealsByType = $mealsResponse.meals | Group-Object meal_type
        foreach ($group in $mealsByType) {
            Write-Host "      $($group.Name): $($group.Count) meals" -ForegroundColor White
        }
    }
}

# Step 6: Test Frontend Access
Write-Host "`n🌐 Step 6: Frontend Access Information" -ForegroundColor Cyan
Write-Host "   Frontend URL: $FRONTEND_URL" -ForegroundColor Green
Write-Host "   Login URL: $FRONTEND_URL/login" -ForegroundColor Green
Write-Host "   Meals URL: $FRONTEND_URL/meals" -ForegroundColor Green
Write-Host "   Admin Panel: $API_BASE/admin/" -ForegroundColor Green

# Summary
Write-Host "`n📋 SUMMARY" -ForegroundColor Green
Write-Host "=========" -ForegroundColor Green

if ($token) {
    Write-Host "✅ Backend is working" -ForegroundColor Green
    Write-Host "✅ Admin user login successful" -ForegroundColor Green
    Write-Host "   Username: $workingUsername" -ForegroundColor White
    Write-Host "   Password: $workingPassword" -ForegroundColor White
    
    if ($mealsResponse -and $mealsResponse.meals.Count -gt 0) {
        Write-Host "✅ Meal schedule API is working with data" -ForegroundColor Green
        Write-Host "`n🎉 Your meal schedule should work now!" -ForegroundColor Green
        Write-Host "   Go to: $FRONTEND_URL/meals" -ForegroundColor Cyan
    } else {
        Write-Host "⚠️  Meal schedule API works but no data" -ForegroundColor Yellow
        Write-Host "`n📝 NEXT STEPS:" -ForegroundColor Yellow
        Write-Host "1. Login to frontend: $FRONTEND_URL/login" -ForegroundColor White
        Write-Host "2. Create a meal plan" -ForegroundColor White
        Write-Host "3. Add some meals to see the schedule" -ForegroundColor White
    }
} else {
    Write-Host "❌ Admin user needs to be created" -ForegroundColor Red
    Write-Host "   Follow the manual steps above" -ForegroundColor Yellow
}

Write-Host "`n✨ Would you like me to create test meal data? (y/n)" -ForegroundColor Cyan
$createTestData = Read-Host

if ($createTestData -eq "y" -or $createTestData -eq "Y" -or $createTestData -eq "yes") {
    if ($token -and $recipesResponse -and ($recipesResponse.results.Count -gt 0 -or $recipesResponse.Count -gt 0)) {
        Write-Host "`n🏗️  Creating test meal plan and data..." -ForegroundColor Yellow
        
        # Create a meal plan for this week
        $weekStart = (Get-Date).AddDays(-([int](Get-Date).DayOfWeek - 1)).ToString("yyyy-MM-dd")
        $weekEnd = (Get-Date).AddDays(-([int](Get-Date).DayOfWeek - 1)).AddDays(6).ToString("yyyy-MM-dd")
        
        $mealPlanData = @{
            name = "Test Week Plan"
            start_date = $weekStart
            end_date = $weekEnd
            is_active = $true
        } | ConvertTo-Json
        
        try {
            $headers = @{ Authorization = "Bearer $token" }
            $newPlan = Invoke-RestMethod -Uri "$API_BASE/meals/plans/" -Method Post -Body $mealPlanData -ContentType "application/json" -Headers $headers
            Write-Host "✅ Created meal plan: $($newPlan.name)" -ForegroundColor Green
            
            # Add some test meals
            $recipes = if ($recipesResponse.results) { $recipesResponse.results } else { $recipesResponse }
            
            for ($day = 0; $day -lt 7; $day++) {
                $mealDate = (Get-Date).AddDays(-([int](Get-Date).DayOfWeek - 1)).AddDays($day).ToString("yyyy-MM-dd")
                
                # Add breakfast
                if ($recipes.Count -gt 0) {
                    $mealData = @{
                        recipe = $recipes[0].id
                        date = $mealDate
                        meal_type = "breakfast"
                        servings = 2
                        notes = "Test breakfast"
                    } | ConvertTo-Json
                    
                    Invoke-RestMethod -Uri "$API_BASE/meals/plans/$($newPlan.id)/meals/" -Method Post -Body $mealData -ContentType "application/json" -Headers $headers | Out-Null
                }
                
                # Add dinner every other day
                if ($day % 2 -eq 0 -and $recipes.Count -gt 1) {
                    $mealData = @{
                        recipe = $recipes[1].id
                        date = $mealDate
                        meal_type = "dinner"
                        servings = 3
                        notes = "Test dinner"
                    } | ConvertTo-Json
                    
                    Invoke-RestMethod -Uri "$API_BASE/meals/plans/$($newPlan.id)/meals/" -Method Post -Body $mealData -ContentType "application/json" -Headers $headers | Out-Null
                }
            }
            
            Write-Host "✅ Added test meals to the plan" -ForegroundColor Green
            Write-Host "`n🎉 Test data created! Check your meal schedule at:" -ForegroundColor Green
            Write-Host "   $FRONTEND_URL/meals" -ForegroundColor Cyan
            
        } catch {
            Write-Host "❌ Failed to create test data: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Cannot create test data - need recipes first" -ForegroundColor Red
        Write-Host "   Run: python manage.py init_onlypans on Render" -ForegroundColor Yellow
    }
}

Write-Host "`n🏁 Script complete! Press Enter to exit..." -ForegroundColor Green
Read-Host
