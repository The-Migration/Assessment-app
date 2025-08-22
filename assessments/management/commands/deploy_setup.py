from django.core.management.base import BaseCommand
from django.db import transaction
from assessments.models import Assessment, Question, AssessmentQuestion, Designation, QuestionCategory
from users.models import CustomUser
import os


class Command(BaseCommand):
    help = 'Set up database for deployment - create missing links and ensure data integrity'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of all links',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting deployment setup...'))
        
        # Check if we're in production (Render)
        is_production = os.environ.get('RENDER', False)
        if is_production:
            self.stdout.write(self.style.WARNING('Running in production environment'))
        
        with transaction.atomic():
            # 1. Ensure we have the basic categories
            self.stdout.write('Setting up question categories...')
            iq_category, created = QuestionCategory.objects.get_or_create(
                name='IQ',
                defaults={'description': 'Intelligence Quotient questions'}
            )
            if created:
                self.stdout.write(f'  + Created IQ category')
            
            cultural_category, created = QuestionCategory.objects.get_or_create(
                name='Cultural',
                defaults={'description': 'Cultural knowledge questions'}
            )
            if created:
                self.stdout.write(f'  + Created Cultural category')
            
            # 2. Ensure we have designations
            self.stdout.write('Setting up designations...')
            designations = {
                'Manager': 'Management level positions',
                'Executive': 'Executive level positions',
                'Entry': 'Entry level positions',
            }
            
            for name, description in designations.items():
                designation, created = Designation.objects.get_or_create(
                    name=name,
                    defaults={'description': description, 'is_active': True}
                )
                if created:
                    self.stdout.write(f'  + Created designation: {name}')
            
            # 3. Fix question links
            self.stdout.write('Fixing question links...')
            assessments = Assessment.objects.all()
            questions = Question.objects.all()
            
            total_links_created = 0
            
            for assessment in assessments:
                self.stdout.write(f'  Processing assessment: {assessment.name}')
                
                # Get questions that match this assessment's type
                matching_questions = questions.filter(assessment_type=assessment.assessment_type)
                
                for question in matching_questions:
                    # Check if link already exists
                    link_exists = AssessmentQuestion.objects.filter(
                        assessment=assessment,
                        question=question
                    ).exists()
                    
                    if not link_exists or options['force']:
                        if options['force'] and link_exists:
                            # Remove existing link
                            AssessmentQuestion.objects.filter(
                                assessment=assessment,
                                question=question
                            ).delete()
                        
                        # Create new link
                        AssessmentQuestion.objects.create(
                            assessment=assessment,
                            question=question,
                            order=AssessmentQuestion.objects.filter(assessment=assessment).count() + 1
                        )
                        total_links_created += 1
                        self.stdout.write(f'    + Linked question {question.id} to assessment {assessment.name}')
            
            # 4. Ensure we have an admin user
            self.stdout.write('Checking admin user...')
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
            admin_user, created = CustomUser.objects.get_or_create(
                email=admin_email,
                defaults={
                    'username': 'admin',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'role': 'admin',
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            if created:
                self.stdout.write(f'  + Created admin user: {admin_email}')
            else:
                self.stdout.write(f'  ✓ Admin user exists: {admin_email}')
            
            # 5. Print summary
            self.stdout.write(self.style.SUCCESS(f'\nDeployment setup completed!'))
            self.stdout.write(f'  - Total question links created: {total_links_created}')
            self.stdout.write(f'  - Total assessments: {assessments.count()}')
            self.stdout.write(f'  - Total questions: {questions.count()}')
            self.stdout.write(f'  - Total AssessmentQuestion links: {AssessmentQuestion.objects.count()}')
            
            if is_production:
                self.stdout.write(self.style.SUCCESS('Production database is now ready!'))
