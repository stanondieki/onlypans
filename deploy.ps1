# PowerShell deployment script for Windows
Write-Host "🚀 Deploying OnlyPans to Render and Vercel..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "render.yaml")) {
    Write-Host "❌ render.yaml not found. Make sure you're in the project root." -ForegroundColor Red
    exit 1
}

# Commit and push changes
Write-Host "📝 Committing changes..." -ForegroundColor Yellow
git add .
$commitMessage = "Deploy OnlyPans - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
git commit -m $commitMessage
git push

Write-Host "✅ Deployment initiated!" -ForegroundColor Green
Write-Host "🔗 Backend URL: https://onlypans-backend.onrender.com" -ForegroundColor Cyan
Write-Host "🔗 Frontend: Deploy to Vercel manually or connect GitHub repo" -ForegroundColor Cyan

Write-Host "`n📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Check Render dashboard for backend deployment progress"
Write-Host "2. Deploy frontend to Vercel by connecting your GitHub repo"
Write-Host "3. Update frontend environment variables in Vercel dashboard"
