from django.core.management.base import BaseCommand
from django.core import serializers
from assessments.models import Assessment, Question, AssessmentSession, Answer, Designation, QuestionCategory
from users.models import CustomUser
import json
from datetime import datetime

class Command(BaseCommand):
    help = 'Backup all assessment data to JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='Output file path',
            default=f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        
        self.stdout.write('Starting data backup...')
        
        # Get all data
        data = {
            'assessments': serializers.serialize('json', Assessment.objects.all()),
            'questions': serializers.serialize('json', Question.objects.all()),
            'sessions': serializers.serialize('json', AssessmentSession.objects.all()),
            'answers': serializers.serialize('json', Answer.objects.all()),
            'designations': serializers.serialize('json', Designation.objects.all()),
            'categories': serializers.serialize('json', QuestionCategory.objects.all()),
            'users': serializers.serialize('json', CustomUser.objects.all()),
        }
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.stdout.write(
            self.style.SUCCESS(f'Backup completed: {output_file}')
        )
        
        # Print summary
        self.stdout.write(f'Backed up:')
        self.stdout.write(f'  - {Assessment.objects.count()} assessments')
        self.stdout.write(f'  - {Question.objects.count()} questions')
        self.stdout.write(f'  - {AssessmentSession.objects.count()} sessions')
        self.stdout.write(f'  - {Answer.objects.count()} answers')
        self.stdout.write(f'  - {CustomUser.objects.count()} users')
