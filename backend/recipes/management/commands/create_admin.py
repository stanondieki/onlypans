from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
import os


class Command(BaseCommand):
    help = 'Create a production-ready superuser account'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username for the superuser (default: admin)',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email for the superuser',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the superuser (or set ADMIN_PASSWORD env var)',
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email'] or f'{username}@onlypans.com'
        password = options['password'] or os.environ.get('ADMIN_PASSWORD')
        
        if not password:
            password = 'OnlyPans2025!'  # Default strong password
            self.stdout.write(
                self.style.WARNING(f'Using default password: {password}')
            )
            self.stdout.write(
                self.style.WARNING('Please change this password after first login!')
            )
        
        # Check if superuser already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists.')
            )
            return
        
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='OnlyPans',
            last_name='Admin'
        )
        
        # Create or update user profile
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'bio': 'OnlyPans System Administrator',
                'cooking_skill_level': 'expert',
                'activity_level': 'moderately_active',
                'weight_goal': 'maintain',
                'notifications_enabled': True,
                'meal_reminders': True,
                'shopping_reminders': True,
                'recipe_recommendations': True,
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Superuser "{username}" created successfully!')
        )
        self.stdout.write(
            self.style.HTTP_INFO(f'Email: {email}')
        )
        self.stdout.write(
            self.style.HTTP_INFO(f'Password: {password}')
        )
        self.stdout.write(
            self.style.WARNING('Remember to change the password after first login!')
        )
