from django.contrib.auth.backends import BaseBackend
from users.models import CustomUser

class FirstLastNameBackend(BaseBackend):
    def authenticate(self, request, first_name=None, last_name=None):
        try:
            user = CustomUser.objects.get(
                first_name__iexact=first_name, 
                last_name__iexact=last_name, 
                role='candidate'
            )
            return user
        except CustomUser.DoesNotExist:
            return None
        except CustomUser.MultipleObjectsReturned:
            # If duplicates exist, return the most recent one
            # This handles legacy data until duplicates are cleaned up
            user = CustomUser.objects.filter(
                first_name__iexact=first_name, 
                last_name__iexact=last_name, 
                role='candidate'
            ).order_by('-date_joined').first()
            return user
            
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None 