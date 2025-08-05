import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlypans_backend.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@onlypans.com', 'admin123')
    print("Superuser 'admin' created successfully!")
else:
    print("Superuser 'admin' already exists.")
