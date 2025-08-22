from django.core.management.base import BaseCommand
from django.db import transaction
from assessments.models import Assessment, Question, AssessmentQuestion, AssessmentSession
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Debug and fix assessment data issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Fix data issues automatically',
        )
        parser.add_argument(
            '--assessment-id',
            type=int,
            help='Debug specific assessment by ID',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting assessment data debug...'))
        
        if options['assessment_id']:
            self.debug_specific_assessment(options['assessment_id'], options['fix'])
        else:
            self.debug_all_assessments(options['fix'])

    def debug_specific_assessment(self, assessment_id, fix=False):
        try:
            assessment = Assessment.objects.get(id=assessment_id)
            self.stdout.write(f'\n=== Assessment: {assessment.name} (ID: {assessment.id}) ===')
            
            # Check questions
            questions = assessment.assessment_questions.all()
            self.stdout.write(f'Linked questions: {questions.count()}')
            
            for aq in questions:
                self.stdout.write(f'  - Question {aq.question.id}: {aq.question.text[:50]}...')
            
            # Check sessions
            sessions = assessment.sessions.all()
            self.stdout.write(f'Total sessions: {sessions.count()}')
            
            for session in sessions:
                self.stdout.write(f'  - Session {session.id}: {session.user.username} - {session.status}')
            
            if fix:
                self.fix_assessment_issues(assessment)
                
        except Assessment.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Assessment with ID {assessment_id} not found'))

    def debug_all_assessments(self, fix=False):
        assessments = Assessment.objects.all()
        self.stdout.write(f'\nFound {assessments.count()} assessments')
        
        for assessment in assessments:
            self.stdout.write(f'\n--- {assessment.name} (ID: {assessment.id}) ---')
            
            # Check questions
            questions = assessment.assessment_questions.all()
            self.stdout.write(f'  Questions: {questions.count()}')
            
            # Check sessions
            sessions = assessment.sessions.all()
            self.stdout.write(f'  Sessions: {sessions.count()}')
            
            if fix:
                self.fix_assessment_issues(assessment)

    def fix_assessment_issues(self, assessment):
        """Fix common assessment data issues"""
        self.stdout.write(f'Fixing issues for assessment: {assessment.name}')
        
        # Check for orphaned AssessmentQuestion records
        orphaned_aqs = AssessmentQuestion.objects.filter(assessment=assessment).exclude(
            question__in=Question.objects.all()
        )
        if orphaned_aqs.exists():
            self.stdout.write(f'  Found {orphaned_aqs.count()} orphaned AssessmentQuestion records')
            if self.confirm_fix():
                orphaned_aqs.delete()
                self.stdout.write(self.style.SUCCESS('  Removed orphaned records'))
        
        # Check for questions without AssessmentQuestion links
        questions_without_links = Question.objects.filter(
            assessment_type=assessment.assessment_type
        ).exclude(
            assessment_questions__assessment=assessment
        )
        if questions_without_links.exists():
            self.stdout.write(f'  Found {questions_without_links.count()} questions without links')
            if self.confirm_fix():
                for question in questions_without_links:
                    AssessmentQuestion.objects.get_or_create(
                        assessment=assessment,
                        question=question,
                        defaults={'order': 0, 'points': question.points}
                    )
                self.stdout.write(self.style.SUCCESS('  Created missing links'))

    def confirm_fix(self):
        """Ask user for confirmation"""
        return input('Fix this issue? (y/N): ').lower().startswith('y')
