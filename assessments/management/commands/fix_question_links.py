from django.core.management.base import BaseCommand
from django.db import transaction
from assessments.models import Assessment, Question, AssessmentQuestion, Designation

class Command(BaseCommand):
    help = 'Fix missing question-to-assessment links'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting question link fix...'))
        
        assessments = Assessment.objects.all()
        questions = Question.objects.all()
        
        self.stdout.write(f'Found {assessments.count()} assessments')
        self.stdout.write(f'Found {questions.count()} questions')
        self.stdout.write(f'Current AssessmentQuestion links: {AssessmentQuestion.objects.count()}')
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        created_links = 0
        
        for assessment in assessments:
            self.stdout.write(f'\n--- Assessment: {assessment.name} (Type: {assessment.assessment_type.name}) ---')
            
            # Find questions that match this assessment's type
            matching_questions = questions.filter(assessment_type=assessment.assessment_type)
            self.stdout.write(f'  Questions matching assessment type: {matching_questions.count()}')
            
            for question in matching_questions:
                # Check if link already exists
                existing_link = AssessmentQuestion.objects.filter(
                    assessment=assessment,
                    question=question
                ).first()
                
                if existing_link:
                    self.stdout.write(f'    ✓ Question {question.id} already linked')
                else:
                    self.stdout.write(f'    + Question {question.id} needs linking')
                    
                    if not options['dry_run']:
                        AssessmentQuestion.objects.create(
                            assessment=assessment,
                            question=question,
                            order=0,
                            points=question.points
                        )
                        created_links += 1
                        self.stdout.write(self.style.SUCCESS(f'      Created link'))
        
        if not options['dry_run']:
            self.stdout.write(self.style.SUCCESS(f'\nCreated {created_links} new question links'))
            self.stdout.write(f'Total AssessmentQuestion links now: {AssessmentQuestion.objects.count()}')
        else:
            self.stdout.write(self.style.WARNING(f'\nWould create {created_links} new question links'))
