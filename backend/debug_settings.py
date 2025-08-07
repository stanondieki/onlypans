import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlypans_backend.production_settings')
django.setup()

print("=== DJANGO SETTINGS DEBUG ===")
print(f"Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE', 'Not set')}")
print(f"DEBUG: {settings.DEBUG}")
print(f"CORS_ALLOW_ALL_ORIGINS: {getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', 'Not found')}")
print(f"CORS_ALLOWED_ORIGINS: {getattr(settings, 'CORS_ALLOWED_ORIGINS', 'Not found')}")
print(f"CORS_ALLOW_CREDENTIALS: {getattr(settings, 'CORS_ALLOW_CREDENTIALS', 'Not found')}")
print(f"Installed apps: {[app for app in settings.INSTALLED_APPS if 'cors' in app.lower()]}")
print(f"Middleware: {[mw for mw in settings.MIDDLEWARE if 'cors' in mw.lower()]}")
