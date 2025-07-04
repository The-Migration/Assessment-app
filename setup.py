#!/usr/bin/env python
"""
Setup script for Assessment Management System
This script helps with initial project setup and data creation.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from assessments.models import Designation, QuestionCategory

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assessment_web.settings')
    django.setup()

def create_sample_data():
    """Create sample assessment types and questions"""
    from assessments.models import Designation, QuestionCategory, Question
    from users.models import CustomUser
    
    print("Creating sample data...")
    
    # Create assessment types
    iq_type, created = Designation.objects.get_or_create(
        name="IQ Test",
        defaults={"description": "IQ Test for candidates"}
    )
    if created:
        print(f"✓ Created assessment type: {iq_type.name}")
    
    cultural_type, created = Designation.objects.get_or_create(
        name="Cultural Assessment",
        defaults={"description": "Cultural fit assessment"}
    )
    if created:
        print(f"✓ Created assessment type: {cultural_type.name}")
    
    # Create question categories
    iq_categories = [
        ('Logical Reasoning', 'Questions testing logical thinking'),
        ('Numerical Ability', 'Mathematical and numerical problems'),
        ('Verbal Ability', 'Language and vocabulary questions'),
    ]
    
    for cat_name, cat_desc in iq_categories:
        category, created = QuestionCategory.objects.get_or_create(
            name=cat_name,
            designation=iq_type,
            defaults={'description': cat_desc}
        )
        if created:
            print(f"✓ Created category: {category.name}")
    
    cultural_categories = [
        ('Work Style', 'Questions about preferred work environment'),
        ('Values', 'Questions about personal and professional values'),
        ('Communication', 'Questions about communication preferences'),
    ]
    
    for cat_name, cat_desc in cultural_categories:
        category, created = QuestionCategory.objects.get_or_create(
            name=cat_name,
            designation=cultural_type,
            defaults={'description': cat_desc}
        )
        if created:
            print(f"✓ Created category: {category.name}")
    
    # Create sample questions
    sample_questions = [
        # IQ Test Questions
        {
            'designation': iq_type,
            'category': QuestionCategory.objects.get(name='Logical Reasoning', designation=iq_type),
            'text': 'If all Bloops are Razzles and all Razzles are Lazzles, then all Bloops are definitely Lazzles.',
            'question_type': 'TF',
            'correct_answer': 'True',
            'difficulty': 'medium',
            'points': 1,
        },
        {
            'designation': iq_type,
            'category': QuestionCategory.objects.get(name='Numerical Ability', designation=iq_type),
            'text': 'What is the next number in the sequence: 2, 6, 12, 20, 30, ?',
            'question_type': 'MCQ',
            'options': ['40', '42', '44', '46'],
            'correct_answer': '42',
            'difficulty': 'medium',
            'points': 2,
        },
        {
            'designation': iq_type,
            'category': QuestionCategory.objects.get(name='Verbal Ability', designation=iq_type),
            'text': 'Choose the word that best completes the analogy: Book is to Reading as Fork is to:',
            'question_type': 'MCQ',
            'options': ['Cooking', 'Eating', 'Kitchen', 'Food'],
            'correct_answer': 'Eating',
            'difficulty': 'easy',
            'points': 1,
        },
        
        # Cultural Assessment Questions
        {
            'designation': cultural_type,
            'category': QuestionCategory.objects.get(name='Work Style', designation=cultural_type),
            'text': 'I prefer to work in a quiet, focused environment.',
            'question_type': 'TF',
            'correct_answer': 'True',
            'difficulty': 'easy',
            'points': 1,
        },
        {
            'designation': cultural_type,
            'category': QuestionCategory.objects.get(name='Values', designation=cultural_type),
            'text': 'What is most important to you in a workplace?',
            'question_type': 'MCQ',
            'options': ['Competitive environment', 'Collaborative teamwork', 'Individual recognition', 'Work-life balance'],
            'correct_answer': 'Collaborative teamwork',
            'difficulty': 'medium',
            'points': 2,
        },
        {
            'designation': cultural_type,
            'category': QuestionCategory.objects.get(name='Communication', designation=cultural_type),
            'text': 'Describe your preferred communication style when working with team members.',
            'question_type': 'SA',
            'correct_answer': 'Open and direct communication',
            'difficulty': 'medium',
            'points': 3,
        },
    ]
    
    for q_data in sample_questions:
        question, created = Question.objects.get_or_create(
            text=q_data['text'],
            designation=q_data['designation'],
            defaults={
                'category': q_data['category'],
                'question_type': q_data['question_type'],
                'options': q_data.get('options'),
                'correct_answer': q_data['correct_answer'],
                'difficulty': q_data['difficulty'],
                'points': q_data['points'],
            }
        )
        if created:
            print(f"✓ Created question: {question.text[:50]}...")
    
    print("Sample data creation completed!")

def create_demo_users():
    """Create demo users for testing"""
    User = get_user_model()
    
    print("Creating demo users...")
    
    demo_users = [
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'admin123',
            'first_name': 'System',
            'last_name': 'Administrator',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'username': 'hr_admin',
            'email': 'hr@example.com',
            'password': 'hr123',
            'first_name': 'HR',
            'last_name': 'Manager',
            'role': 'hr_admin',
            'is_staff': True,
        },
        {
            'username': 'candidate1',
            'email': 'candidate1@example.com',
            'password': 'candidate123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'candidate',
        },
        {
            'username': 'candidate2',
            'email': 'candidate2@example.com',
            'password': 'candidate123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'candidate',
        },
        {
            'username': 'reviewer',
            'email': 'reviewer@example.com',
            'password': 'reviewer123',
            'first_name': 'Review',
            'last_name': 'Manager',
            'role': 'reviewer',
        },
    ]
    
    for user_data in demo_users:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'role': user_data['role'],
                'is_staff': user_data.get('is_staff', False),
                'is_superuser': user_data.get('is_superuser', False),
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"✓ Created user: {user.username} ({user.get_role_display()})")
        else:
            print(f"⚠ User already exists: {user.username}")
    
    print("Demo users creation completed!")

def main():
    """Main setup function"""
    print("Assessment Management System - Setup Script")
    print("=" * 50)
    
    try:
        setup_django()
        print("✓ Django environment setup completed")
        
        # Run migrations
        print("\nRunning database migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ Database migrations completed")
        
        # Create sample data
        print("\nCreating sample data...")
        create_sample_data()
        
        # Create demo users
        print("\nCreating demo users...")
        create_demo_users()
        
        print("\n" + "=" * 50)
        print("Setup completed successfully!")
        print("\nDemo Users:")
        print("- Admin: admin / admin123")
        print("- HR Admin: hr_admin / hr123")
        print("- Candidate 1: candidate1 / candidate123")
        print("- Candidate 2: candidate2 / candidate123")
        print("- Reviewer: reviewer / reviewer123")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000/admin/")
        print("3. Login with admin credentials")
        print("4. Start creating assessments!")
        
    except Exception as e:
        print(f"Error during setup: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 