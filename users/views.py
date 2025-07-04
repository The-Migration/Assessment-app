from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, AdminSignupForm, AUTHORIZED_ADMIN_EMAILS
from django.contrib.auth import login
from django.contrib import messages
from users.forms import CandidateNameLoginForm, CandidateSignupForm
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def candidate_name_login(request):
    if request.method == 'POST':
        form = CandidateNameLoginForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = authenticate(request, first_name=first_name, last_name=last_name)
            if user is not None:
                login(request, user)
                return redirect('assessments:candidate_portal')
            else:
                messages.error(request, 'No candidate found with that name.')
    else:
        form = CandidateNameLoginForm()
    return render(request, 'registration/candidate_name_login.html', {'form': form})

def candidate_signup(request):
    if request.method == 'POST':
        form = CandidateSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='users.backends.FirstLastNameBackend')
            return redirect('assessments:candidate_portal')
    else:
        form = CandidateSignupForm()
    return render(request, 'registration/candidate_signup.html', {'form': form})

def admin_signup(request):
    """Admin signup view that only allows authorized email"""
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Admin account created successfully! You can now login.')
            return redirect('admin_login')
    else:
        form = AdminSignupForm()
    return render(request, 'registration/admin_signup.html', {'form': form})

class AdminLoginView(LoginView):
    """Custom admin login view that only allows authorized emails"""
    template_name = 'registration/admin_login.html'
    
    def form_valid(self, form):
        """Override to check if user has an authorized email"""
        user = form.get_user()
        
        # Check if user has an authorized email and is admin
        if user.email not in AUTHORIZED_ADMIN_EMAILS:
            messages.error(self.request, 'Access denied. Only authorized administrators can access this system.')
            return self.form_invalid(form)
        
        if user.role != 'admin':
            messages.error(self.request, 'Access denied. This account does not have admin privileges.')
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to admin dashboard after successful login"""
        return reverse_lazy('assessments:admin_dashboard')

class CustomLogoutView(LogoutView):
    """Custom logout view that redirects based on user role"""
    template_name = 'registration/logout_success.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Store user role before logout"""
        if request.user.is_authenticated:
            self.user_was_admin = request.user.role == 'admin'
        else:
            self.user_was_admin = False
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Add user role context to template"""
        context = super().get_context_data(**kwargs)
        context['user_was_admin'] = getattr(self, 'user_was_admin', False)
        return context