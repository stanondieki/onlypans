#!/usr/bin/env bash
# Render deployment script

echo "Starting OnlyPans Backend Deployment..."

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Create default superuser if none exists
echo "Creating default superuser..."
python manage.py create_default_superuser

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "Starting Gunicorn server..."
gunicorn onlypans_backend.wsgi:application --bind 0.0.0.0:$PORT
