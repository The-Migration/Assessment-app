from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('hr_admin', 'HR Admin'),
        ('candidate', 'Candidate'),
        ('reviewer', 'Reviewer'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

    @property
    def is_admin(self):
        return self.role in ['admin', 'hr_admin']

    @property
    def is_candidate(self):
        return self.role == 'candidate'

    @property
    def is_reviewer(self):
        return self.role == 'reviewer' 