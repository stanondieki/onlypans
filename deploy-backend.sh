#!/bin/bash
# Backend deployment script for Render

echo "🚀 Deploying OnlyPans Backend to Render..."

# Check if we're in the right directory
if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml not found. Make sure you're in the project root."
    exit 1
fi

# Commit and push changes
echo "📝 Committing changes..."
git add .
git commit -m "Deploy backend to Render - $(date '+%Y-%m-%d %H:%M:%S')"
git push

echo "✅ Backend deployment initiated! Check Render dashboard for progress."
echo "🔗 Backend URL: https://onlypans-backend.onrender.com"
