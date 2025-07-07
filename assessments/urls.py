from django.urls import path
from . import views

app_name = 'assessments'

urlpatterns = [
    # Home and main views
    path('', views.home, name='home'),
    
    # Admin views
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/assessments/', views.assessment_list, name='assessment_list'),
    path('admin/assessments/create/', views.assessment_create, name='assessment_create'),
    path('admin/assessments/<int:assessment_id>/', views.assessment_detail, name='assessment_detail'),
    path('admin/questions/', views.question_list, name='question_list'),
    path('admin/questions/create/', views.question_create, name='question_create'),
    path('admin/questions/<int:question_id>/', views.question_detail, name='question_detail'),
    path('admin/questions/<int:question_id>/edit/', views.question_edit, name='question_edit'),
    path('admin/questions/<int:question_id>/delete/', views.question_delete, name='question_delete'),
    path('admin/sessions/', views.session_list, name='session_list'),
    path('admin/sessions/<int:session_id>/', views.session_detail, name='session_detail'),
    path('admin/analytics/', views.analytics, name='analytics'),
    path('admin/assessments/<int:assessment_id>/add-questions/', views.add_existing_question, name='add_existing_question'),
    path('admin/assessment-questions/<int:assessment_question_id>/remove/', views.remove_assessment_question, name='remove_assessment_question'),
    path('admin/questions/bulk-import/', views.bulk_import_questions, name='bulk_import_questions'),
    path('admin/assessments/<int:assessment_id>/bulk-import/', views.bulk_import_questions, name='bulk_import_questions_for_assessment'),
    path('admin/export/assessment-results/excel/', views.export_assessment_results_excel, name='export_assessment_results_excel'),
    path('admin/export/assessment-results/pdf/', views.export_assessment_results_pdf, name='export_assessment_results_pdf'),
    path('admin/analytics/report/', views.analytics_report, name='analytics_report'),
    path('admin/assign-assessment/', views.assign_assessment, name='assign_assessment'),
    path('admin/assessments/<int:assessment_id>/edit/', views.assessment_edit, name='assessment_edit'),
    path('admin/assessments/<int:assessment_id>/delete/', views.assessment_delete, name='assessment_delete'),
    path('admin/assessment-results/<int:session_id>/', views.assessment_results, name='assessment_results'),
    
    # Candidate views
    path('candidate-welcome/', views.candidate_welcome, name='candidate_welcome'),
    path('candidate-portal/', views.candidate_portal, name='candidate_portal'),
    path('start-assessment/<int:assessment_id>/', views.start_assessment, name='start_assessment'),
    path('take-assessment/<int:session_id>/', views.take_assessment, name='take_assessment'),
    path('submit-assessment/<int:session_id>/', views.submit_assessment, name='submit_assessment'),
    path('assessment-completed/<int:session_id>/', views.assessment_completed, name='assessment_completed'),
    path('begin-assigned-session/<int:session_id>/', views.begin_assigned_session, name='begin_assigned_session'),
    
    # AJAX endpoints
    path('ajax/save-answer/', views.save_answer_ajax, name='save_answer_ajax'),
]