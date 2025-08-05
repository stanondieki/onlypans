#!/usr/bin/env python
"""
OnlyPans Production Initialization Script
Run this script to set up your OnlyPans instance with live data
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlypans_backend.production_settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from recipes.models import Recipe, RecipeTag
from accounts.models import UserProfile


def main():
    print("🍳 OnlyPans Production Initialization")
    print("=" * 40)
    
    # Step 1: Apply migrations
    print("\n📦 Applying database migrations...")
    try:
        call_command('migrate', verbosity=0)
        print("✅ Database migrations applied successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    # Step 2: Collect static files
    print("\n📁 Collecting static files...")
    try:
        call_command('collectstatic', '--noinput', verbosity=0)
        print("✅ Static files collected successfully")
    except Exception as e:
        print(f"❌ Static file collection failed: {e}")
        return False
    
    # Step 3: Create admin user
    print("\n👤 Creating admin user...")
    try:
        if not User.objects.filter(username='admin').exists():
            call_command('create_admin', verbosity=1)
        else:
            print("ℹ️ Admin user already exists")
    except Exception as e:
        print(f"❌ Admin user creation failed: {e}")
        return False
    
    # Step 4: Initialize OnlyPans data
    print("\n🍽️ Initializing OnlyPans data...")
    try:
        call_command('init_onlypans', verbosity=1)
    except Exception as e:
        print(f"❌ OnlyPans initialization failed: {e}")
        return False
    
    # Step 5: Create test user for demonstrations
    print("\n🧪 Creating demo user...")
    create_demo_user()
    
    # Step 6: Display summary
    print("\n📊 Initialization Summary:")
    print("=" * 40)
    
    recipe_count = Recipe.objects.count()
    tag_count = RecipeTag.objects.count()
    user_count = User.objects.filter(is_active=True).count()
    
    print(f"✅ Recipes created: {recipe_count}")
    print(f"✅ Recipe tags created: {tag_count}")
    print(f"✅ Active users: {user_count}")
    
    print("\n🚀 OnlyPans is ready for production!")
    print("\nAccess your admin panel at: /admin/")
    print("Default admin credentials:")
    print("  Username: admin")
    print("  Password: OnlyPans2025!")
    print("\n⚠️ Remember to change the admin password!")
    
    return True


def create_demo_user():
    """Create a demo user for testing and demonstrations"""
    try:
        demo_user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@onlypans.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'is_active': True
            }
        )
        
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            
            # Create profile for demo user
            UserProfile.objects.get_or_create(
                user=demo_user,
                defaults={
                    'bio': 'Demo user for OnlyPans showcase',
                    'cooking_skill_level': 'beginner',
                    'activity_level': 'moderately_active',
                    'weight_goal': 'maintain',
                    'dietary_restrictions': 'none',
                    'favorite_cuisines': ['italian', 'american'],
                    'notifications_enabled': True,
                    'meal_reminders': True,
                    'shopping_reminders': True,
                    'recipe_recommendations': True,
                }
            )
            print("✅ Demo user created successfully")
        else:
            print("ℹ️ Demo user already exists")
            
    except Exception as e:
        print(f"⚠️ Demo user creation failed: {e}")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
