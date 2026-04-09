from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db import connection

class CustomAuthBackend(BaseBackend):
    """
    Custom authentication backend that works with the custom users table
    but is compatible with Django's authentication system
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, user, password FROM users WHERE user = %s AND password = %s", [username, password])
                user_data = cursor.fetchone()
                
                if user_data:
                    user_id, db_username, db_password = user_data
                    
                    # Create or get a Django User object (without password)
                    user, created = User.objects.get_or_create(
                        username=db_username,
                        defaults={
                            'email': db_username,
                            'is_active': True,
                            'is_staff': False,
                            'is_superuser': False,
                        }
                    )
                    
                    # Store custom user info in session
                    if request:
                        request.session['custom_user_id'] = user_id
                        request.session['custom_username'] = db_username
                        request.session.save()
                    
                    return user
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
