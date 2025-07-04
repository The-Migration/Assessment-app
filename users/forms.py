from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# Authorized admin emails
AUTHORIZED_ADMIN_EMAILS = [
    'zainab.akram@themigration.com.au',
    'hr@istudywise.com',
    'nauman@istudywise.com',
    'careers@themigration.com.au',
    'sheyral@themigration.com.au'
]

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

class CandidateNameLoginForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

class CandidateSignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name')

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        if first_name and last_name:
            # Check if a candidate with this name already exists
            existing_user = CustomUser.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name,
                role='candidate'
            ).first()
            
            if existing_user:
                raise forms.ValidationError(
                    f"A candidate with the name '{first_name} {last_name}' already exists. "
                    "Please use the login page instead."
                )
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'candidate'
        # Generate a unique username from first and last name
        base_username = f"{user.first_name.lower()}{user.last_name.lower()}"
        username = base_username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username
        user.set_unusable_password()
        if commit:
            user.save()
        return user

class AdminSignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Enter a strong password"
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Enter the same password again"
    )
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email not in AUTHORIZED_ADMIN_EMAILS:
            raise forms.ValidationError(
                "Access denied. Only authorized email addresses can create admin accounts."
            )
        
        # Check if user with this email already exists
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists. Please use the login page instead."
            )
        
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken. Please choose a different one."
            )
        
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("The two password fields didn't match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'admin'
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        return user
