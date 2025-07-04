from django.core.management.base import BaseCommand
from django.db.models import Count
from users.models import CustomUser
from assessments.models import AssessmentSession


class Command(BaseCommand):
    help = 'Clean up duplicate candidate users, keeping the most recent one'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Find duplicate candidates (same first_name and last_name)
        duplicates = (
            CustomUser.objects
            .filter(role='candidate')
            .values('first_name', 'last_name')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        if not duplicates:
            self.stdout.write(
                self.style.SUCCESS('No duplicate candidate users found.')
            )
            return

        total_to_delete = 0
        
        for duplicate in duplicates:
            first_name = duplicate['first_name']
            last_name = duplicate['last_name']
            count = duplicate['count']
            
            self.stdout.write(
                f"Found {count} users named '{first_name} {last_name}'"
            )
            
            # Get all users with this name, ordered by date_joined (newest first)
            users = CustomUser.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name,
                role='candidate'
            ).order_by('-date_joined')
            
            # Keep the first (most recent) user, delete the rest
            users_to_keep = users.first()
            users_to_delete = users[1:]
            
            self.stdout.write(
                f"  Keeping: {users_to_keep.username} (ID: {users_to_keep.id}, Created: {users_to_keep.date_joined})"
            )
            
            for user in users_to_delete:
                # Check if user has any assessment sessions
                sessions = AssessmentSession.objects.filter(user=user)
                session_count = sessions.count()
                
                if session_count > 0:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Would delete: {user.username} (ID: {user.id}) - "
                            f"Has {session_count} assessment sessions"
                        )
                    )
                    if not dry_run:
                        # Transfer sessions to the user we're keeping
                        sessions.update(user=users_to_keep)
                        self.stdout.write(
                            f"    Transferred {session_count} sessions to {users_to_keep.username}"
                        )
                else:
                    self.stdout.write(
                        f"  Would delete: {user.username} (ID: {user.id}) - No assessment data"
                    )
                
                if not dry_run:
                    user.delete()
                    self.stdout.write(
                        self.style.SUCCESS(f"    Deleted: {user.username}")
                    )
                
                total_to_delete += 1

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"DRY RUN: Would delete {total_to_delete} duplicate users. "
                    "Run without --dry-run to actually delete them."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully cleaned up {total_to_delete} duplicate users."
                )
            )
