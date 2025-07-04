from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Assessment, Question, AssessmentSession, Answer, Designation, QuestionCategory
from users.models import CustomUser

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['name', 'description', 'assessment_type', 'time_limit_minutes', 
                 'pass_threshold', 'max_attempts', 'allow_retake', 'show_results_immediately',
                 'randomize_questions', 'is_active', 'instructions']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 4}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['assessment_type', 'category', 'text', 'question_type', 'options', 
                 'correct_answer', 'explanation', 'points', 'is_active']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'explanation': forms.Textarea(attrs={'rows': 2}),
            'options': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter options as JSON array: ["Option 1", "Option 2", "Option 3", "Option 4"]', 'style': 'display: none;'}),
            'correct_answer': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_options(self):
        options = self.cleaned_data.get('options')
        question_type = self.cleaned_data.get('question_type')
        print(f"clean_options called - question_type: {question_type}, options: {options!r}")
        if question_type == 'MCQ':
            if not options or options == 'null':
                print("MCQ question but no options provided")
                raise forms.ValidationError("Options are required for Multiple Choice questions.")
            try:
                import json
                # If options is already a list (edit), use it directly
                if isinstance(options, list):
                    options_list = options
                else:
                    options_list = json.loads(options)
                print(f"Parsed options: {options_list}")
                if not isinstance(options_list, list) or len(options_list) < 2:
                    print(f"Invalid options format: {options_list}")
                    raise forms.ValidationError("At least 2 options are required for MCQ questions.")
            except (json.JSONDecodeError, TypeError) as e:
                print(f"JSON decode error: {e}")
                raise forms.ValidationError("Options must be a valid JSON array.")
        return options

    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get('question_type')
        options = cleaned_data.get('options')
        correct_answer = cleaned_data.get('correct_answer')
        
        if question_type == 'MCQ':
            # For MCQ, validate that correct_answer is one of the options
            if options and correct_answer:
                try:
                    import json
                    options_list = json.loads(options)
                    if correct_answer not in options_list:
                        raise forms.ValidationError("Correct answer must be one of the provided options.")
                except (json.JSONDecodeError, TypeError):
                    pass  # This will be caught by clean_options
        else:
            # For non-MCQ questions, correct_answer is required
            if not correct_answer:
                raise forms.ValidationError("Correct answer is required for this question type.")
        
        return cleaned_data

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name', 'description']

class QuestionCategoryForm(forms.ModelForm):
    class Meta:
        model = QuestionCategory
        fields = ['name', 'description', 'assessment_type']

class AnswerForm(forms.Form):
    response = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=True
    )

class MCQAnswerForm(forms.Form):
    response = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True
    )

    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if question.question_type == 'MCQ' and question.options:
            options = question.get_options_list()
            choices = [(option, option) for option in options]
            self.fields['response'].choices = choices

class TrueFalseAnswerForm(forms.Form):
    response = forms.ChoiceField(
        choices=[('True', 'True'), ('False', 'False')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True
    )

class AssessmentSessionForm(forms.ModelForm):
    class Meta:
        model = AssessmentSession
        fields = ['assessment']

class BulkQuestionImportForm(forms.Form):
    file = forms.FileField(
        label='Upload Excel/CSV File',
        help_text='File should contain columns: text, question_type, correct_answer, difficulty, points, designation, category'
    )

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, initial='candidate')
    phone = forms.CharField(required=False)
    department = forms.CharField(required=False)
    employee_id = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 
                 'role', 'phone', 'department', 'employee_id')

class AssessmentSearchForm(forms.Form):
    assessment_type = forms.ModelChoiceField(
        queryset=Designation.objects.filter(is_active=True),
        required=False,
        empty_label="All Designations"
    )
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search assessments...'}))
    is_active = forms.ChoiceField(
        choices=[('', 'All'), ('True', 'Active'), ('False', 'Inactive')],
        required=False,
        label='Status'
    )

class QuestionSearchForm(forms.Form):
    assessment_type = forms.ModelChoiceField(
        queryset=Designation.objects.all(),
        required=False,
        empty_label="All Designations"
    )
    category = forms.ModelChoiceField(
        queryset=QuestionCategory.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    question_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Question.QUESTION_TYPES,
        required=False
    )
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search questions...'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assessment_type'].queryset = Designation.objects.all()
        self.fields['category'].queryset = QuestionCategory.objects.all()

class AssignAssessmentForm(forms.Form):
    candidate = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='candidate'),
        label='Select Candidate',
        help_text='Choose the candidate to assign this assessment to'
    )
    assessment = forms.ModelChoiceField(
        queryset=Assessment.objects.filter(is_active=True),
        label='Select Assessment',
        help_text='Choose the assessment to assign'
    )