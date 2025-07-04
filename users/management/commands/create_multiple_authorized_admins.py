from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.forms import AUTHORIZED_ADMIN_EMAILS

User = get_user_model()

class Command(BaseCommand):
    help = 'Create admin users for all authorized emails'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Password for all admin accounts (default: admin123)'
        )
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update existing users to admin role if they exist'
        )

    def handle(self, *args, **options):
        password = options['password']
        update_existing = options['update_existing']
        
        created_count = 0
        updated_count = 0
        
        for email in AUTHORIZED_ADMIN_EMAILS:
            # Generate username from email
            username = email.split('@')[0].replace('.', '')
            
            # Extract first and last name from email
            name_part = email.split('@')[0]
            if '.' in name_part:
                first_name, last_name = name_part.split('.', 1)
                first_name = first_name.capitalize()
                last_name = last_name.capitalize()
            else:
                first_name = name_part.capitalize()
                last_name = ''
            
            # Check if user already exists
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'admin',
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created admin user: {username} ({email})'
                    )
                )
            else:
                if update_existing:
                    # Update existing user to admin
                    user.role = 'admin'
                    user.is_staff = True
                    user.is_superuser = True
                    user.is_active = True
                    user.set_password(password)
                    user.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'Updated existing user to admin: {username} ({email})'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'User already exists: {username} ({email}) - use --update-existing to update'
                        )
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: {created_count} admin users created, {updated_count} users updated'
            )
        )
        
        if created_count > 0 or updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Default password for all admin accounts: {password}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'Please change passwords after first login for security.'
                )
            ) 