from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser
import json

class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'

    def __str__(self):
        return self.name

class QuestionCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    assessment_type = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='categories')
    
    class Meta:
        verbose_name = 'Question Category'
        verbose_name_plural = 'Question Categories'
        unique_together = ['name', 'assessment_type']

    def __str__(self):
        return f"{self.name} - {self.assessment_type.name}"

class Question(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer'),
    ]
    
    assessment_type = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='questions')
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    text = models.TextField()
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES)
    options = models.JSONField(null=True, blank=True, help_text="For MCQ: list of options")
    correct_answer = models.TextField()
    explanation = models.TextField(blank=True, help_text="Explanation for the correct answer")
    points = models.PositiveIntegerField(default=1, help_text="Points for this question")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f"{self.text[:50]}... - {self.get_question_type_display()}"

    def get_options_list(self):
        """Return options as a list for MCQ questions"""
        if self.question_type == 'MCQ' and self.options:
            return json.loads(self.options) if isinstance(self.options, str) else self.options
        return []

class Assessment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assessment_type = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='assessments')
    questions = models.ManyToManyField(Question, through='AssessmentQuestion', related_name='assessments')
    time_limit_minutes = models.PositiveIntegerField(default=60)
    randomize_questions = models.BooleanField(default=True)
    pass_threshold = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Pass threshold as percentage (0-100)"
    )
    max_attempts = models.PositiveIntegerField(default=1, help_text="Maximum attempts allowed")
    allow_retake = models.BooleanField(default=True, help_text="Allow candidates to retake this assessment")
    show_results_immediately = models.BooleanField(default=True, help_text="Show results immediately after completion")
    is_active = models.BooleanField(default=True)
    instructions = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_assessments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Assessment'
        verbose_name_plural = 'Assessments'

    def __str__(self):
        return self.name

    def get_total_points(self):
        """Calculate total points for this assessment"""
        return sum(aq.points for aq in self.assessment_questions.all())

    def get_question_count(self):
        """Get total number of questions"""
        return self.assessment_questions.count()
    
    @property
    def total_points(self):
        """Property to get total points for this assessment"""
        return self.get_total_points()
    
    @property
    def estimated_time(self):
        """Property to get estimated time based on question count"""
        question_count = self.get_question_count()
        # Estimate 2 minutes per question
        return question_count * 2

class AssessmentQuestion(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='assessment_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='assessment_questions')
    order = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['order']
        unique_together = ['assessment', 'question']

    def __str__(self):
        return f"{self.assessment.name} - {self.question.text[:30]}..."

class AssessmentSession(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assessment_sessions')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='sessions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken_minutes = models.PositiveIntegerField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    total_points = models.PositiveIntegerField(null=True, blank=True)
    percentage_score = models.FloatField(null=True, blank=True)
    passed = models.BooleanField(null=True, blank=True)
    attempt_number = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = 'Assessment Session'
        verbose_name_plural = 'Assessment Sessions'
        unique_together = ['user', 'assessment', 'attempt_number']

    def __str__(self):
        return f"{self.user.username} - {self.assessment.name} (Attempt {self.attempt_number})"

    def calculate_score(self):
        """Calculate and update the session score"""
        answers = self.answers.all()
        total_points = 0
        earned_points = 0
        
        for answer in answers:
            # Get points from AssessmentQuestion relationship
            try:
                assessment_question = self.assessment.assessment_questions.get(question=answer.question)
                question_points = assessment_question.points
            except AssessmentQuestion.DoesNotExist:
                # Fallback to question's default points
                question_points = answer.question.points
            
            total_points += question_points
            if answer.is_correct:
                earned_points += question_points
        
        self.total_points = total_points
        self.score = earned_points
        self.percentage_score = (earned_points / total_points * 100) if total_points > 0 else 0
        self.passed = self.percentage_score >= self.assessment.pass_threshold
        self.save()

class Answer(models.Model):
    session = models.ForeignKey(AssessmentSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    response = models.TextField()
    is_correct = models.BooleanField(null=True, blank=True)
    points_earned = models.PositiveIntegerField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        unique_together = ['session', 'question']

    def __str__(self):
        return f"{self.session.user.username} - {self.question.text[:30]}..."

    def check_answer(self):
        """Check if the answer is correct and update points"""
        if self.question.question_type == 'MCQ':
            self.is_correct = self.response.strip().lower() == self.question.correct_answer.strip().lower()
        elif self.question.question_type == 'TF':
            self.is_correct = self.response.strip().lower() == self.question.correct_answer.strip().lower()
        else:
            # For other types, manual review might be needed
            self.is_correct = None
        
        # Get points from AssessmentQuestion relationship
        try:
            assessment_question = self.session.assessment.assessment_questions.get(question=self.question)
            question_points = assessment_question.points
        except AssessmentQuestion.DoesNotExist:
            # Fallback to question's default points
            question_points = self.question.points
        
        if self.is_correct:
            self.points_earned = question_points
        else:
            self.points_earned = 0
        
        self.save()
        return self.is_correct
