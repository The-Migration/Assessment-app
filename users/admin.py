from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUser
from .forms import AUTHORIZED_ADMIN_EMAILS

class RestrictedAdminSite(AdminSite):
    """Custom admin site that restricts access to authorized emails only"""
    
    def login(self, request, extra_context=None):
        """Override login to check authorized emails"""
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if username and password:
                user = authenticate(request, username=username, password=password)
                if user and user.email not in AUTHORIZED_ADMIN_EMAILS:
                    messages.error(request, 'Access denied. Only authorized administrators can access Django admin.')
                    return redirect('/admin/login/')
        
        return super().login(request, extra_context)

# Create custom admin site instance
admin_site = RestrictedAdminSite(name='restricted_admin')

@admin.register(CustomUser, site=admin_site)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'employee_id')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'department', 'employee_id')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

# Also register with default admin for backward compatibility but add restriction
@admin.register(CustomUser)
class DefaultCustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'employee_id')
    ordering = ('-created_at',)
    
    def has_module_permission(self, request):
        """Restrict access to authorized emails only"""
        if not super().has_module_permission(request):
            return False
        return (request.user.is_authenticated and 
                request.user.email in AUTHORIZED_ADMIN_EMAILS)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'department', 'employee_id')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
