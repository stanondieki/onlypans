"""
Quick admin user creation script
Run this in Render shell to create the admin user
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlypans_backend.production_settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    print("🔐 Creating OnlyPans Admin User")
    print("=" * 35)
    
    # Check if admin already exists
    if User.objects.filter(username='admin').exists():
        print("ℹ️ Admin user already exists!")
        admin_user = User.objects.get(username='admin')
        print(f"Username: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        return
    
    # Create the admin user
    try:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@onlypans.com',
            password='OnlyPans2025!',
            first_name='OnlyPans',
            last_name='Admin'
        )
        
        print("✅ Admin user created successfully!")
        print(f"Username: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        print("Password: OnlyPans2025!")
        print("")
        print("🌐 Admin Panel: https://onlypans.onrender.com/admin/")
        print("⚠️ Please change the password after first login!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

if __name__ == "__main__":
    create_admin_user()
