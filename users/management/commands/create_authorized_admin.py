from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Create or update the authorized admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            help='Set a specific password for the admin user',
            default='admin123'
        )

    def handle(self, *args, **options):
        authorized_email = 'zainab.akram@themigration.com.au'
        password = options['password']
        
        with transaction.atomic():
            # Check if user with this email already exists
            user, created = User.objects.get_or_create(
                email=authorized_email,
                defaults={
                    'username': 'zainab.akram',
                    'first_name': 'Zainab',
                    'last_name': 'Akram',
                    'role': 'admin',
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True,
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created authorized admin user: {authorized_email}'
                    )
                )
            else:
                # Update existing user to ensure correct settings
                user.role = 'admin'
                user.is_staff = True
                user.is_superuser = True
                user.is_active = True
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated authorized admin user: {authorized_email}'
                    )
                )
            
            # Deactivate any other admin users that don't have the authorized email
            other_admins = User.objects.filter(role='admin').exclude(email=authorized_email)
            if other_admins.exists():
                count = other_admins.count()
                other_admins.update(role='candidate', is_staff=False, is_superuser=False)
                self.stdout.write(
                    self.style.WARNING(
                        f'Converted {count} unauthorized admin account(s) to candidate accounts'
                    )
                )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Admin setup complete. Login credentials:'
                )
            )
            self.stdout.write(f'Email: {authorized_email}')
            self.stdout.write(f'Username: {user.username}')
            self.stdout.write(f'Password: {password}') 