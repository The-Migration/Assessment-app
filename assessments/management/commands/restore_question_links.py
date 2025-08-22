from django.core.management.base import BaseCommand
from assessments.models import Assessment, Question, AssessmentQuestion


class Command(BaseCommand):
    help = 'Restore missing question links for assessments'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting question link restoration...'))
        
        assessments = Assessment.objects.all()
        questions = Question.objects.all()
        
        total_links_created = 0
        
        for assessment in assessments:
            self.stdout.write(f'Processing assessment: {assessment.name}')
            
            # Get questions that match this assessment's type
            matching_questions = questions.filter(assessment_type=assessment.assessment_type)
            
            for question in matching_questions:
                # Check if link already exists
                link_exists = AssessmentQuestion.objects.filter(
                    assessment=assessment,
                    question=question
                ).exists()
                
                if not link_exists:
                    # Create new link
                    AssessmentQuestion.objects.create(
                        assessment=assessment,
                        question=question,
                        order=AssessmentQuestion.objects.filter(assessment=assessment).count() + 1
                    )
                    total_links_created += 1
                    self.stdout.write(f'  + Linked question {question.id} to assessment {assessment.name}')
                else:
                    self.stdout.write(f'  ✓ Question {question.id} already linked to assessment {assessment.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\nRestoration completed!'))
        self.stdout.write(f'Total links created: {total_links_created}')
        self.stdout.write(f'Total AssessmentQuestion links now: {AssessmentQuestion.objects.count()}')
