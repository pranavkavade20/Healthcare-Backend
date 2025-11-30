from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that uses email instead of username.
    This allows users to log in with their email address.
    """
    
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        """
        Authenticate using email or username (for backward compatibility).
        """
        # Support both email and username parameters
        identifier = email or username
        
        if not identifier or not password:
            return None
        
        try:
            # Try to find user by email first
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            try:
                # Fall back to username if email not found
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                return None
        
        # Check password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        """Get a user by ID."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
