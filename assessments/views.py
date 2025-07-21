from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.http import HttpResponseRedirect
import json
from datetime import datetime, timedelta
import csv
from io import TextIOWrapper
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

from .models import (
    Assessment, AssessmentSession, Question, Answer, Designation, 
    QuestionCategory, AssessmentQuestion
)
from .forms import (
    AssessmentForm, QuestionForm, AnswerForm, MCQAnswerForm, TrueFalseAnswerForm,
    DesignationForm, QuestionCategoryForm, BulkQuestionImportForm,
    AssessmentSearchForm, QuestionSearchForm, UserRegistrationForm, AssignAssessmentForm
)
from users.models import CustomUser
from users.forms import AUTHORIZED_ADMIN_EMAILS

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_candidate(user):
    return user.is_authenticated and user.role == 'candidate'

def is_authorized_admin(user):
    """Check if user is admin with authorized email"""
    return (user.is_authenticated and 
            user.role == 'admin' and 
            user.email in AUTHORIZED_ADMIN_EMAILS)

def admin_required(view_func):
    """Custom decorator that redirects to admin login for admin views and checks authorized email"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('admin_login'))
        if not is_authorized_admin(request.user):
            messages.error(request, 'Access denied. Only authorized administrators can access this system.')
            return HttpResponseRedirect(reverse('admin_login'))
        return view_func(request, *args, **kwargs)
    return wrapper

def candidate_welcome(request):
    """Welcome page for candidates - directs to signup first"""
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('assessments:admin_dashboard')
        elif request.user.role == 'candidate':
            return redirect('assessments:candidate_portal')
    return render(request, 'assessments/candidate_welcome.html')

@login_required
def home(request):
    """Home page with role-based redirects"""
    if request.user.role == 'admin':
        return redirect('assessments:admin_dashboard')
    elif request.user.role == 'candidate':
        return redirect('assessments:candidate_portal')
    else:
        return redirect('assessments:candidate_welcome')  # Changed to welcome page

@admin_required
def admin_dashboard(request):
    """Admin dashboard with overview statistics"""
    # Get statistics
    total_assessments = Assessment.objects.count()
    total_questions = Question.objects.count()
    total_users = CustomUser.objects.count()
    total_sessions = AssessmentSession.objects.count()
    
    # Recent activity
    recent_sessions = AssessmentSession.objects.select_related('user', 'assessment').order_by('-started_at')[:10]
    recent_assessments = Assessment.objects.order_by('-created_at')[:5]
    
    # Assessment type distribution
    designations = Designation.objects.annotate(
        assessment_count=Count('assessments', distinct=True),
        question_count=Count('questions', distinct=True)
    )
    
    # Calculate percentages for progress bars
    for designation in designations:
        if total_assessments > 0:
            designation.percentage = (designation.assessment_count / total_assessments) * 100
        else:
            designation.percentage = 0
    
    context = {
        'total_assessments': total_assessments,
        'total_questions': total_questions,
        'total_users': total_users,
        'total_sessions': total_sessions,
        'recent_sessions': recent_sessions,
        'recent_assessments': recent_assessments,
        'designations': designations,
    }
    return render(request, 'assessments/admin_dashboard.html', context)

@login_required
@user_passes_test(is_candidate)
def candidate_portal(request):
    """Candidate portal showing available assessments"""
    # Get available assessments for the user
    available_assessments = Assessment.objects.filter(is_active=True)
    
    # Get user's assessment sessions
    user_sessions = AssessmentSession.objects.filter(user=request.user).select_related('assessment')
    
    # Check which assessments can be taken and their status
    for assessment in available_assessments:
        user_attempts = user_sessions.filter(assessment=assessment).count()
        assessment.can_take = user_attempts < assessment.max_attempts
        assessment.attempts_remaining = assessment.max_attempts - user_attempts
        assessment.last_attempt = user_sessions.filter(assessment=assessment).order_by('-started_at').first()
        
        # Check if there's an in-progress session for this assessment
        in_progress_session = user_sessions.filter(assessment=assessment, status='in_progress').first()
        if in_progress_session:
            assessment.in_progress_session = in_progress_session
            assessment.can_take = False  # Can't start new if one is in progress
        else:
            assessment.in_progress_session = None
    
    context = {
        'available_assessments': available_assessments,
        'user_sessions': user_sessions,
    }
    return render(request, 'assessments/candidate_portal.html', context)

@login_required
@user_passes_test(is_candidate)
def start_assessment(request, assessment_id):
    """Start a new assessment session"""
    assessment = get_object_or_404(Assessment, id=assessment_id, is_active=True)
    
    # Check if user can take this assessment
    existing_sessions = AssessmentSession.objects.filter(
        user=request.user, 
        assessment=assessment
    ).count()
    
    if existing_sessions >= assessment.max_attempts:
        messages.error(request, f"You have already taken this assessment {assessment.max_attempts} times.")
        return redirect('assessments:candidate_portal')
    
    # Create new session
    session = AssessmentSession.objects.create(
        user=request.user,
        assessment=assessment,
        status='in_progress'
    )
    
    return redirect('assessments:take_assessment', session_id=session.id)

@login_required
@user_passes_test(is_candidate)
def take_assessment(request, session_id):
    """Take an assessment with timer and question navigation"""
    session = get_object_or_404(AssessmentSession, id=session_id, user=request.user)
    
    if session.status == 'completed':
        messages.info(request, "This assessment has already been completed.")
        return redirect('assessments:assessment_completed', session_id=session.id)
    
    # Get questions for this assessment
    questions = session.assessment.assessment_questions.select_related('question').order_by('order')
    
    if not questions.exists():
        messages.error(request, "No questions found for this assessment.")
        return redirect('assessments:candidate_portal')
    
    # Handle form submission
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        response = request.POST.get('response')
        
        if question_id and response:
            question = get_object_or_404(Question, id=question_id)
            
            # Save or update answer
            answer, created = Answer.objects.get_or_create(
                session=session,
                question=question,
                defaults={'response': response}
            )
            if not created:
                answer.response = response
                answer.save()
            
            # Check if answer is correct
            answer.check_answer()
    
    # Get current question (first unanswered or first question)
    answered_questions = session.answers.values_list('question_id', flat=True)
    current_question = None
    
    for aq in questions:
        if aq.question.id not in answered_questions:
            current_question = aq.question
            break
    
    if not current_question:
        current_question = questions.first().question
    
    # Prepare answers_dict for template
    answers_dict = {a.question_id: a.response for a in session.answers.all()}

    # Calculate progress
    total_questions = questions.count()
    answered_count = answered_questions.count()
    progress = (answered_count / total_questions) * 100 if total_questions > 0 else 0
    
    # Calculate remaining time
    time_limit = session.assessment.time_limit_minutes
    elapsed = timezone.now() - session.started_at
    remaining_minutes = max(0, time_limit - elapsed.total_seconds() / 60)
    
    next_question_index = answered_count + 1
    context = {
        'session': session,
        'current_question': current_question,
        'questions': questions,
        'progress': progress,
        'answered_count': answered_count,
        'total_questions': total_questions,
        'remaining_minutes': int(remaining_minutes),
        'time_limit': time_limit,
        'answers_dict': answers_dict,
        'next_question_index': next_question_index,
    }
    return render(request, 'assessments/take_assessment.html', context)

@login_required
@user_passes_test(is_candidate)
def submit_assessment(request, session_id):
    """Submit and complete an assessment"""
    session = get_object_or_404(AssessmentSession, id=session_id, user=request.user)
    
    if session.status == 'completed':
        messages.info(request, "Assessment already submitted.")
        return redirect('assessments:assessment_completed', session_id=session.id)
    
    # Calculate score
    session.calculate_score()
    
    # Update session status
    session.status = 'completed'
    session.completed_at = timezone.now()
    session.time_taken_minutes = int((session.completed_at - session.started_at).total_seconds() / 60)
    session.save()
    
    messages.success(request, "Assessment submitted successfully!")
    return redirect('assessments:assessment_completed', session_id=session.id)

@login_required
@user_passes_test(is_candidate)
def assessment_completed(request, session_id):
    """Show assessment completion confirmation to candidate"""
    session = get_object_or_404(AssessmentSession, id=session_id, user=request.user)
    
    context = {
        'session': session,
    }
    return render(request, 'assessments/assessment_completed.html', context)

@admin_required
def assessment_results(request, session_id):
    """Show assessment results - Admin only"""
    session = get_object_or_404(AssessmentSession, id=session_id)
    
    # Get answers with questions
    answers = session.answers.select_related('question').all()
    
    context = {
        'session': session,
        'answers': answers,
    }
    return render(request, 'assessments/assessment_results.html', context)

@admin_required
def assessment_list(request):
    """Admin view for managing assessments"""
    form = AssessmentSearchForm(request.GET)
    assessments = Assessment.objects.all()  # Show all by default

    if form.is_valid():
        if form.cleaned_data.get('designation'):
            assessments = assessments.filter(designation=form.cleaned_data['designation'])
        if form.cleaned_data.get('search'):
            assessments = assessments.filter(
                Q(name__icontains=form.cleaned_data['search']) |
                Q(description__icontains=form.cleaned_data['search'])
            )
        is_active_val = form.cleaned_data.get('is_active')
        if is_active_val != '' and is_active_val is not None:
            assessments = assessments.filter(is_active=(is_active_val == 'True'))

    # Pagination
    paginator = Paginator(assessments.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'assessments/assessment_list.html', context)

@admin_required
def assessment_create(request):
    """Create new assessment"""
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.created_by = request.user
            assessment.save()
            messages.success(request, "Assessment created successfully!")
            return redirect('assessments:assessment_detail', assessment_id=assessment.id)
    else:
        form = AssessmentForm()
    
    context = {'form': form}
    return render(request, 'assessments/assessment_form.html', context)

@admin_required
def assessment_detail(request, assessment_id):
    """View assessment details"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    questions = assessment.assessment_questions.select_related('question').order_by('order')
    sessions = assessment.sessions.select_related('user').order_by('-started_at')[:10]
    
    context = {
        'assessment': assessment,
        'questions': questions,
        'sessions': sessions,
    }
    return render(request, 'assessments/assessment_detail.html', context)

@admin_required
def question_list(request):
    """Admin view for managing questions"""
    print('GET parameters:', request.GET)
    form = QuestionSearchForm(request.GET)
    print('Form is valid:', form.is_valid())
    if hasattr(form, 'cleaned_data'):
        print('Cleaned data:', form.cleaned_data)
    if hasattr(form, 'errors') and form.errors:
        print('Form errors:', form.errors)
    questions = Question.objects.all()
    
    if form.is_valid():
        if form.cleaned_data.get('designation'):
            questions = questions.filter(assessment_type=form.cleaned_data['designation'])
        # Custom logic for IQ/Cultural tabs
        category_id = request.GET.get('category')
        if category_id:
            try:
                selected_category = QuestionCategory.objects.get(id=category_id)
                # If the selected category is 'IQ' or 'Cultural', filter for all categories with that name
                if selected_category.name.lower() in ['iq', 'cultural']:
                    questions = questions.filter(category__name__iexact=selected_category.name)
                else:
                    questions = questions.filter(category=selected_category)
            except QuestionCategory.DoesNotExist:
                pass
        elif form.cleaned_data.get('category'):
            questions = questions.filter(category=form.cleaned_data['category'])
        if form.cleaned_data.get('question_type'):
            questions = questions.filter(question_type=form.cleaned_data['question_type'])
        if form.cleaned_data.get('search'):
            questions = questions.filter(text__icontains=form.cleaned_data['search'])
    
    # Pagination
    paginator = Paginator(questions.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch all designations for tabs
    designations = Designation.objects.all()
    categories = QuestionCategory.objects.all()
    selected_designation_id = None
    selected_category_id = None
    if form.is_valid():
        if form.cleaned_data.get('assessment_type'):
            selected_designation_id = form.cleaned_data['assessment_type'].id
        if form.cleaned_data.get('category'):
            selected_category_id = form.cleaned_data['category'].id

    # Get IQ and Cultural category IDs
    iq_category = categories.filter(name__iexact='IQ').first()
    cultural_category = categories.filter(name__iexact='Cultural').first()
    iq_category_id = iq_category.id if iq_category else None
    cultural_category_id = cultural_category.id if cultural_category else None

    context = {
        'page_obj': page_obj,
        'form': form,
        'designations': designations,
        'selected_designation_id': selected_designation_id,
        'categories': categories,
        'selected_category_id': selected_category_id,
        'iq_category_id': iq_category_id,
        'cultural_category_id': cultural_category_id,
    }
    return render(request, 'assessments/question_list.html', context)

@admin_required
@require_POST
def bulk_delete_questions(request):
    """Bulk delete selected questions"""
    question_ids = request.POST.getlist('question_ids')
    if not question_ids:
        messages.error(request, "No questions selected for deletion.")
        return redirect('assessments:question_list')
    deleted_count = 0
    for qid in question_ids:
        try:
            question = Question.objects.get(id=qid)
            question.delete()
            deleted_count += 1
        except Question.DoesNotExist:
            continue
    messages.success(request, f"Deleted {deleted_count} question(s) successfully!")
    return redirect('assessments:question_list')

@admin_required
def question_create(request):
    """Create new question, optionally link to an assessment if designation_id is provided"""
    designation_id = request.GET.get('designation_id') or request.POST.get('designation_id')
    initial = {}
    if designation_id:
        try:
            designation = Designation.objects.get(id=designation_id)
            initial['designation'] = designation.designation
        except Designation.DoesNotExist:
            designation = None
    else:
        designation = None

    if request.method == 'POST':
        form = QuestionForm(request.POST, initial=initial)
        if form.is_valid():
            text = form.cleaned_data['text']
            question_type = form.cleaned_data['question_type']
            assessment_type = form.cleaned_data['assessment_type']
            # Check for duplicate by text, type, and assessment_type
            existing_question = Question.objects.filter(text=text, question_type=question_type, assessment_type=assessment_type).first()
            if existing_question:
                messages.warning(request, "A question with the same text, type, and assessment type already exists.")
                # Optionally, link to assessment if not already linked
                if designation and not AssessmentQuestion.objects.filter(assessment=designation, question=existing_question).exists():
                    AssessmentQuestion.objects.create(assessment=designation, question=existing_question)
                    messages.success(request, "Existing question linked to assessment!")
                return redirect('assessments:assessment_detail', assessment_id=designation.id) if designation else redirect('assessments:question_list')
            question = form.save()
            # Link to assessment if designation_id is provided and not already linked
            if designation:
                from .models import AssessmentQuestion
                if not AssessmentQuestion.objects.filter(assessment=designation, question=question).exists():
                    AssessmentQuestion.objects.create(assessment=designation, question=question)
                    messages.success(request, "Question created and added to assessment!")
                else:
                    messages.info(request, "Question already exists in this assessment.")
                return redirect('assessments:assessment_detail', assessment_id=designation.id)
            messages.success(request, "Question created successfully!")
            return redirect('assessments:question_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = QuestionForm(initial=initial)
    context = {'form': form}
    return render(request, 'assessments/question_form.html', context)

@admin_required
def question_detail(request, question_id):
    """View question details"""
    question = get_object_or_404(Question, id=question_id)
    # Count correct answers and total answers
    correct_count = question.answers.filter(is_correct=True).count()
    total_count = question.answers.count()
    
    context = {
        'question': question,
        'correct_count': correct_count,
        'total_count': total_count,
    }
    return render(request, 'assessments/question_detail.html', context)

@admin_required
def question_edit(request, question_id):
    """Edit existing question"""
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated successfully!")
            return redirect('assessments:question_list')
    else:
        form = QuestionForm(instance=question)
    
    context = {
        'form': form,
        'question': question,
        'is_edit': True,
    }
    return render(request, 'assessments/question_form.html', context)

@admin_required
def question_delete(request, question_id):
    """Delete a question permanently"""
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question_text = question.text[:50]  # Store for success message
        question.delete()
        messages.success(request, f"Question '{question_text}...' deleted successfully!")
        return redirect('assessments:question_list')
    context = {
        'question': question,
    }
    return render(request, 'assessments/question_confirm_delete.html', context)

@admin_required
def session_list(request):
    """Admin view for assessment sessions"""
    sessions = AssessmentSession.objects.select_related('user', 'assessment').order_by('-started_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        sessions = sessions.filter(status=status)
    
    # Pagination
    paginator = Paginator(sessions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status,
    }
    return render(request, 'assessments/session_list.html', context)

@admin_required
def session_detail(request, session_id):
    """View session details and answers"""
    session = get_object_or_404(AssessmentSession, id=session_id)
    answers = session.answers.select_related('question').all()
    
    context = {
        'session': session,
        'answers': answers,
    }
    return render(request, 'assessments/session_detail.html', context)

@admin_required
def analytics(request):
    """Analytics and reporting dashboard"""
    # Completed sessions with proper null handling
    completed_sessions = AssessmentSession.objects.filter(status='completed')
    total_completed_sessions = completed_sessions.count()
    
    # Calculate average score with null handling
    sessions_with_score = completed_sessions.exclude(percentage_score__isnull=True)
    average_score = sessions_with_score.aggregate(avg=Avg('percentage_score'))['avg'] or 0
    
    # Calculate pass rate
    pass_count = completed_sessions.filter(passed=True).count()
    pass_rate = (pass_count * 100.0 / total_completed_sessions) if total_completed_sessions > 0 else 0
    
    total_candidates = CustomUser.objects.filter(role='candidate').count()

    # Assessment performance - use consistent approach
    assessment_performance = []
    for assessment in Assessment.objects.all():
        sessions = assessment.sessions.filter(status='completed')
        completed_count = sessions.count()
        
        # Calculate average score for this assessment
        sessions_with_score = sessions.exclude(percentage_score__isnull=True)
        avg_score = sessions_with_score.aggregate(avg=Avg('percentage_score'))['avg'] or 0
        
        # Calculate pass rate for this assessment
        pass_count = sessions.filter(passed=True).count()
        pass_rate_assessment = (pass_count * 100.0 / completed_count) if completed_count > 0 else 0
        
        # Calculate average time
        avg_time = sessions.aggregate(avg=Avg('time_taken_minutes'))['avg'] or 0
        
        assessment_performance.append({
            'id': assessment.id,
            'name': assessment.name,
            'description': assessment.description,
            'assessment_type': assessment.assessment_type,
            'completed_count': completed_count,
            'avg_score': avg_score,
            'pass_rate': pass_rate_assessment,
            'avg_time': avg_time,
        })

    # Recent results
    recent_results = completed_sessions.select_related('user', 'assessment').order_by('-completed_at')[:10]
    # Add duration_minutes for template
    for result in recent_results:
        result.duration_minutes = result.time_taken_minutes or 0

    context = {
        'total_completed_sessions': total_completed_sessions,
        'average_score': round(average_score, 2),
        'pass_rate': round(pass_rate, 2),
        'total_candidates': total_candidates,
        'assessment_performance': assessment_performance,
        'recent_results': recent_results,
    }
    return render(request, 'assessments/analytics.html', context)

@csrf_exempt
@require_POST
def save_answer_ajax(request):
    """AJAX endpoint to save answers during assessment"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        response = data.get('response')
        
        session = get_object_or_404(AssessmentSession, id=session_id, user=request.user)
        question = get_object_or_404(Question, id=question_id)
        
        # Save or update answer
        answer, created = Answer.objects.get_or_create(
            session=session,
            question=question,
            defaults={'response': response}
        )
        if not created:
            answer.response = response
            answer.save()
        
        # Check answer
        answer.check_answer()
        
        return JsonResponse({'success': True, 'is_correct': answer.is_correct})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@admin_required
def add_existing_question(request, assessment_id):
    """Allow admin to add existing questions to an assessment"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    # Only show questions of the same designation type and not already added
    available_questions = Question.objects.filter(assessment_type=assessment.assessment_type).exclude(assessment_questions__assessment=assessment)
    if request.method == 'POST':
        question_ids = request.POST.getlist('question_ids')
        from .models import AssessmentQuestion
        added_count = 0
        for qid in question_ids:
            try:
                question = Question.objects.get(id=qid)
                # Only add if not already linked
                if not AssessmentQuestion.objects.filter(assessment=assessment, question=question).exists():
                    AssessmentQuestion.objects.create(assessment=assessment, question=question)
                    added_count += 1
            except Question.DoesNotExist:
                continue
        messages.success(request, f"Added {added_count} new question(s) to this assessment.")
        return redirect('assessments:assessment_detail', assessment_id=assessment.id)
    context = {
        'assessment': assessment,
        'available_questions': available_questions,
    }
    return render(request, 'assessments/add_existing_question.html', context)

@admin_required
def remove_assessment_question(request, assessment_question_id):
    aq = get_object_or_404(AssessmentQuestion, id=assessment_question_id)
    assessment_id = aq.assessment.id
    aq.delete()
    return redirect('assessments:assessment_detail', assessment_id=assessment_id)

@admin_required
@require_http_methods(["GET", "POST"])
def bulk_import_questions(request, assessment_id=None):
    """Bulk import questions from a CSV file with preview and select step."""
    from .forms import BulkQuestionImportForm
    import json
    context = {}
    form = BulkQuestionImportForm(request.POST or None, request.FILES or None)
    context['form'] = form
    context['assessment_id'] = assessment_id
    context['success_count'] = 0
    context['error_rows'] = []
    context['results'] = []
    assessment = None
    if assessment_id:
        from .models import Assessment
        assessment = Assessment.objects.filter(id=assessment_id).first()
        context['assessment'] = assessment

    # Step 1: Parse and preview
    if request.method == 'POST' and 'preview' in request.POST and form.is_valid():
        file = request.FILES['file']
        decoded_file = TextIOWrapper(file, encoding='utf-8')
        reader = csv.DictReader(decoded_file)
        preview_questions = []
        for i, row in enumerate(reader, start=2):
            preview_questions.append({
                'row': i,
                'text': row.get('text'),
                'question_type': row.get('question_type'),
                'options': row.get('options'),
                'correct_answer': row.get('correct_answer'),
                'points': row.get('points'),
                'assessment_type': row.get('assessment_type'),
                'category': row.get('category'),
                'raw': row
            })
        # Store preview data in session as JSON
        request.session['bulk_import_preview'] = json.dumps(preview_questions)
        context['preview_questions'] = preview_questions
        context['preview_mode'] = True
        return render(request, 'assessments/bulk_import_questions.html', context)

    # Step 2: Import selected
    if request.method == 'POST' and 'import_selected' in request.POST:
        selected_rows = request.POST.getlist('selected_rows')
        preview_questions = json.loads(request.session.get('bulk_import_preview', '[]'))
        from .models import Question, Designation, QuestionCategory, AssessmentQuestion
        for q in preview_questions:
            if str(q['row']) not in selected_rows:
                continue
            try:
                text = q['text']
                question_type = q['question_type']
                correct_answer = q['correct_answer']
                points = int(q['points'] or 1)
                assessment_type_name = q.get('assessment_type')
                category_name = q['category']
                options = q['options']
                designation = None
                if assessment_type_name:
                    designation, _ = Designation.objects.get_or_create(name=assessment_type_name)
                elif assessment:
                    designation = assessment.assessment_type
                category = None
                if category_name and designation:
                    category, _ = QuestionCategory.objects.get_or_create(name=category_name, assessment_type=designation)
                if question_type == 'MCQ' and options:
                    try:
                        options_list = json.loads(options)
                        if not isinstance(options_list, list):
                            raise ValueError
                    except Exception:
                        options_list = [opt.strip() for opt in options.split(',')]
                    options = json.dumps(options_list)
                else:
                    options = None
                # Check for duplicate by text, type, and assessment_type
                existing_question = Question.objects.filter(text=text, question_type=question_type, assessment_type=designation).first()
                if existing_question:
                    # Only link if not already linked
                    if assessment and not AssessmentQuestion.objects.filter(assessment=assessment, question=existing_question).exists():
                        AssessmentQuestion.objects.create(assessment=assessment, question=existing_question, points=points)
                        context['success_count'] += 1
                        context['results'].append({'row': q['row'], 'question': existing_question})
                    else:
                        context['error_rows'].append({'row': q['row'], 'error': 'Duplicate: Question already exists', 'data': q['raw']})
                    continue
                question = Question.objects.create(
                    assessment_type=designation,
                    category=category,
                    text=text,
                    question_type=question_type,
                    options=options,
                    correct_answer=correct_answer,
                    points=points,
                    is_active=True
                )
                if assessment:
                    # Only add if not already linked
                    if not AssessmentQuestion.objects.filter(assessment=assessment, question=question).exists():
                        AssessmentQuestion.objects.create(assessment=assessment, question=question, points=points)
                        context['success_count'] += 1
                        context['results'].append({'row': q['row'], 'question': question})
                    else:
                        context['error_rows'].append({'row': q['row'], 'error': 'Duplicate: Question already in assessment', 'data': q['raw']})
                else:
                    context['success_count'] += 1
                    context['results'].append({'row': q['row'], 'question': question})
            except Exception as e:
                context['error_rows'].append({'row': q['row'], 'error': str(e), 'data': q['raw']})
        # Clean up session
        if 'bulk_import_preview' in request.session:
            del request.session['bulk_import_preview']
        return render(request, 'assessments/bulk_import_questions.html', context)

    # Default: show upload form
    return render(request, 'assessments/bulk_import_questions.html', context)

@admin_required
def export_assessment_results_excel(request):
    # Export all completed assessment sessions as CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assessment_results.csv"'
    writer = csv.writer(response)
    writer.writerow(['Candidate', 'Assessment', 'Score', 'Total Marks', 'Percentage', 'Passed', 'Completed At'])
    sessions = AssessmentSession.objects.filter(status='completed').select_related('user', 'assessment')
    for s in sessions:
        writer.writerow([
            s.user.username,
            s.assessment.name,
            s.score,
            s.total_points,
            s.percentage_score,
            'Yes' if s.passed else 'No',
            s.completed_at.strftime('%Y-%m-%d %H:%M') if s.completed_at else ''
        ])
    return response

@admin_required
def assign_assessment(request):
    """Assign an assessment to a candidate"""
    if request.method == 'POST':
        form = AssignAssessmentForm(request.POST)
        if form.is_valid():
            candidate = form.cleaned_data['candidate']
            assessment = form.cleaned_data['assessment']
            
            # Check if candidate has already taken this assessment max times
            existing_sessions = AssessmentSession.objects.filter(
                user=candidate, 
                assessment=assessment
            ).count()
            
            if existing_sessions >= assessment.max_attempts:
                messages.error(request, f"{candidate.username} has already been assigned this assessment {assessment.max_attempts} times.")
            else:
                # Create new session
                session = AssessmentSession.objects.create(
                    user=candidate,
                    assessment=assessment,
                    status='not_started'
                )
                messages.success(request, f"Assessment '{assessment.name}' assigned to {candidate.username} successfully!")
                return redirect('assessments:admin_dashboard')
    else:
        form = AssignAssessmentForm()
    
    context = {
        'form': form,
    }
    return render(request, 'assessments/assign_assessment.html', context)

@login_required
@user_passes_test(is_candidate)
def begin_assigned_session(request, session_id):
    """Begin an assigned assessment session (status: not_started)"""
    session = get_object_or_404(AssessmentSession, id=session_id, user=request.user, status='not_started')
    session.status = 'in_progress'
    session.started_at = timezone.now()
    session.save()
    return redirect('assessments:take_assessment', session_id=session.id)

@admin_required
def assessment_edit(request, assessment_id):
    """Edit an existing assessment"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    if request.method == 'POST':
        form = AssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assessment updated successfully!")
            return redirect('assessments:assessment_detail', assessment_id=assessment.id)
    else:
        form = AssessmentForm(instance=assessment)
    context = {'form': form, 'assessment': assessment, 'is_edit': True}
    return render(request, 'assessments/assessment_form.html', context)

@admin_required
def assessment_delete(request, assessment_id):
    """Delete an assessment"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    if request.method == 'POST':
        assessment_name = assessment.name
        assessment.delete()
        messages.success(request, f"Assessment '{assessment_name}' deleted successfully!")
        return redirect('assessments:assessment_list')
    context = {
        'assessment': assessment,
    }
    return render(request, 'assessments/assessment_confirm_delete.html', context)

@admin_required
def export_assessment_results_pdf(request):
    # Export all completed assessment sessions as PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="assessment_results.pdf"'
    
    buffer = []
    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 40, "Assessment Results")
    c.setFont("Helvetica", 10)
    
    sessions = AssessmentSession.objects.filter(status='completed').select_related('user', 'assessment')
    data = [["Candidate", "Assessment", "Score", "Total Marks", "Percentage", "Passed", "Completed At"]]
    for s in sessions:
        data.append([
            s.user.username,
            s.assessment.name,
            s.score,
            s.total_points,
            f"{s.percentage_score:.1f}%",
            "Yes" if s.passed else "No",
            s.completed_at.strftime('%Y-%m-%d %H:%M') if s.completed_at else ''
        ])
    table = Table(data, colWidths=[80, 100, 50, 60, 60, 40, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    table.wrapOn(c, width, height)
    table_height = 20 * len(data)
    table.drawOn(c, 30, height - 80 - table_height)
    c.showPage()
    c.save()
    return response

@admin_required
def analytics_report(request):
    # Render a detailed analytics report as HTML
    # Use the same context as analytics view
    from django.db.models import Avg, Count
    
    # Get completed sessions with proper null handling
    completed_sessions = AssessmentSession.objects.filter(status='completed')
    total_completed_sessions = completed_sessions.count()
    
    # Calculate average score with null handling
    sessions_with_score = completed_sessions.exclude(percentage_score__isnull=True)
    average_score = sessions_with_score.aggregate(avg=Avg('percentage_score'))['avg'] or 0
    
    # Calculate pass rate
    pass_count = completed_sessions.filter(passed=True).count()
    pass_rate = (pass_count * 100.0 / total_completed_sessions) if total_completed_sessions > 0 else 0
    
    total_candidates = CustomUser.objects.filter(role='candidate').count()
    
    # Assessment performance - use consistent approach
    assessment_performance = []
    for assessment in Assessment.objects.all():
        sessions = assessment.sessions.filter(status='completed')
        completed_count = sessions.count()
        
        # Calculate average score for this assessment
        sessions_with_score = sessions.exclude(percentage_score__isnull=True)
        avg_score = sessions_with_score.aggregate(avg=Avg('percentage_score'))['avg'] or 0
        
        # Calculate pass rate for this assessment
        pass_count = sessions.filter(passed=True).count()
        pass_rate_assessment = (pass_count * 100.0 / completed_count) if completed_count > 0 else 0
        
        assessment_performance.append({
            'id': assessment.id,
            'name': assessment.name,
            'description': assessment.description,
            'assessment_type': assessment.assessment_type,
            'completed_count': completed_count,
            'avg_score': avg_score,
            'pass_rate': pass_rate_assessment,
        })
    
    # Calculate average duration in Python
    for assessment_data in assessment_performance:
        assessment = Assessment.objects.get(id=assessment_data['id'])
        sessions = assessment.sessions.filter(status='completed')
        durations = []
        for s in sessions:
            if s.started_at and s.completed_at:
                duration = (s.completed_at - s.started_at).total_seconds() / 60
                durations.append(duration)
        if durations:
            assessment_data['avg_time_minutes'] = sum(durations) / len(durations)
        else:
            assessment_data['avg_time_minutes'] = 0
    
    recent_results = completed_sessions.select_related('user', 'assessment').order_by('-completed_at')[:10]
    
    # Add duration_minutes for template
    for result in recent_results:
        result.duration_minutes = result.time_taken_minutes or 0
    
    context = {
        'total_completed_sessions': total_completed_sessions,
        'average_score': average_score,
        'pass_rate': pass_rate,
        'total_candidates': total_candidates,
        'assessment_performance': assessment_performance,
        'recent_results': recent_results,
    }
    return render(request, 'assessments/analytics_report.html', context)