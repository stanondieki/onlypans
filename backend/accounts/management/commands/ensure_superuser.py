from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Ensure superuser exists with known credentials'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin')
        parser.add_argument('--email', type=str, default='admin@onlypans.com')
        parser.add_argument('--password', type=str, default='admin123')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Check if user already exists
        try:
            user = User.objects.get(username=username)
            # Update password if user exists
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Updated existing user: {username}')
            )
        except User.DoesNotExist:
            # Create new superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created new superuser: {username}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Superuser ready - Username: {username}, Password: {password}')
        )
