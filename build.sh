#!/usr/bin/env bash
# Root-level build script for Render

set -o errexit  # exit on error

echo "🚀 Starting OnlyPans build process..."

# Navigate to backend directory
cd backend

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🗄️  Running database migrations..."
python manage.py migrate

echo "👤 Creating default superuser..."
python manage.py create_default_superuser

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "✅ Build completed successfully!"
