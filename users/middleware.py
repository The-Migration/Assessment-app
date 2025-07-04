from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .forms import AUTHORIZED_ADMIN_EMAILS

class AdminAccessMiddleware:
    """Middleware to restrict admin access to authorized emails only"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if accessing admin areas
        if (request.path.startswith('/admin/') or 
            request.path.startswith('/assessments/admin-dashboard/') or
            request.path.startswith('/assessments/assessment') or
            request.path.startswith('/assessments/question') or
            request.path.startswith('/assessments/analytics')):
            
            if request.user.is_authenticated:
                # Check if user has admin role but not authorized email
                if (request.user.role == 'admin' and 
                    request.user.email not in AUTHORIZED_ADMIN_EMAILS):
                    messages.error(request, 'Access denied. Only authorized administrators can access this system.')
                    return redirect('admin_login')
        
        response = self.get_response(request)
        return response 