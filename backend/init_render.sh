#!/bin/bash

# OnlyPans Production Initialization Script
# This script should be run on the Render server to initialize live data

echo "🍳 OnlyPans Production Initialization"
echo "====================================="

# Change to the backend directory
cd backend

echo ""
echo "📦 Running database migrations..."
python manage.py migrate

echo ""
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "👤 Creating admin user..."
python manage.py create_admin

echo ""
echo "🍽️ Initializing OnlyPans data..."
python manage.py init_onlypans

echo ""
echo "🎉 OnlyPans initialization complete!"
echo ""
echo "📊 Summary:"
echo "✅ Database migrations applied"
echo "✅ Static files collected"
echo "✅ Admin user created"
echo "✅ Recipe tags and starter recipes added"
echo "✅ Demo user created"
echo ""
echo "🌐 Your OnlyPans instance is ready!"
echo "Admin panel: https://onlypans.onrender.com/admin/"
echo "Default admin credentials:"
echo "  Username: admin"
echo "  Password: OnlyPans2025!"
echo ""
echo "⚠️ Remember to change the admin password!"
