from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import (
    Designation, QuestionCategory, Question, Assessment, 
    AssessmentQuestion, AssessmentSession, Answer
)

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        fields = ('text', 'question_type', 'correct_answer', 'difficulty', 'points', 'assessment_type__name', 'category__name')
        export_order = fields

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)

@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'assessment_type', 'description')
    list_filter = ('assessment_type',)
    search_fields = ('name', 'description')
    ordering = ('assessment_type', 'name')

class AssessmentQuestionInline(admin.TabularInline):
    model = AssessmentQuestion
    extra = 1
    ordering = ('order',)

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ('text_preview', 'question_type', 'assessment_type', 'category', 'points', 'is_active')
    list_filter = ('question_type', 'assessment_type', 'category', 'is_active', 'created_at')
    search_fields = ('text', 'correct_answer')
    ordering = ('assessment_type', 'category')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('assessment_type', 'category', 'text', 'question_type')
        }),
        ('Answer Options', {
            'fields': ('options', 'correct_answer', 'explanation'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('difficulty', 'points', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def text_preview(self, obj):
        return obj.text[:100] + "..." if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Question Text'

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'assessment_type', 'time_limit_minutes', 'pass_threshold', 'question_count', 'is_active', 'created_by')
    list_filter = ('assessment_type', 'is_active', 'created_at', 'created_by')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AssessmentQuestionInline]
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'assessment_type', 'instructions')
        }),
        ('Settings', {
            'fields': ('time_limit_minutes', 'randomize_questions', 'pass_threshold', 'max_attempts', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_count(self, obj):
        return obj.get_question_count()
    question_count.short_description = 'Questions'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ('question', 'response', 'is_correct', 'points_earned', 'answered_at')
    can_delete = False

@admin.register(AssessmentSession)
class AssessmentSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'assessment', 'status', 'score', 'percentage_score', 'passed', 'attempt_number', 'started_at')
    list_filter = ('status', 'passed', 'assessment__assessment_type', 'started_at')
    search_fields = ('user__username', 'user__email', 'assessment__name')
    ordering = ('-started_at',)
    readonly_fields = ('user', 'assessment', 'started_at', 'completed_at', 'time_taken_minutes')
    inlines = [AnswerInline]
    
    fieldsets = (
        ('Session Info', {
            'fields': ('user', 'assessment', 'status', 'attempt_number')
        }),
        ('Results', {
            'fields': ('score', 'total_points', 'percentage_score', 'passed')
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'time_taken_minutes')
        }),
    )
    
    actions = ['recalculate_scores']
    
    def recalculate_scores(self, request, queryset):
        for session in queryset:
            session.calculate_score()
        self.message_user(request, f"Recalculated scores for {queryset.count()} sessions.")
    recalculate_scores.short_description = "Recalculate scores for selected sessions"

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'question_preview', 'response_preview', 'is_correct', 'points_earned', 'answered_at')
    list_filter = ('is_correct', 'question__question_type', 'answered_at')
    search_fields = ('session__user__username', 'question__text', 'response')
    ordering = ('-answered_at',)
    readonly_fields = ('session', 'question', 'answered_at')
    
    def question_preview(self, obj):
        return obj.question.text[:50] + "..." if len(obj.question.text) > 50 else obj.question.text
    question_preview.short_description = 'Question'
    
    def response_preview(self, obj):
        return obj.response[:50] + "..." if len(obj.response) > 50 else obj.response
    response_preview.short_description = 'Response'
