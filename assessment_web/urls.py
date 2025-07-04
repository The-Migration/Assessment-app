from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import candidate_name_login, AdminLoginView, admin_signup
from assessments.views import candidate_welcome

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', candidate_welcome, name='home'),  # Default landing page
    path('assessments/', include('assessments.urls')),
    path('users/', include('users.urls')),
    path('accounts/login/', candidate_name_login, name='login'),  # Candidate login
    path('accounts/admin-login/', AdminLoginView.as_view(), name='admin_login'),  # Admin login
    path('accounts/admin-signup/', admin_signup, name='admin_signup'),  # Admin signup
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)