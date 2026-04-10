from django.shortcuts import redirect
from django.conf import settings

class CustomLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define public paths that don't require authentication
        public_paths = [
            '/',
            '/login/',
            '/signup/',
            '/static/',
            '/media/',
            '/admin/',
        ]
        
        # Check if current path is public
        is_public = any(request.path.startswith(path) for path in public_paths)
        
        # Check if user is authenticated via custom session
        if not request.session.get('is_authenticated') and not is_public:
            # Redirect to login page with next parameter
            return redirect(f'/login/?next={request.path}')
        
        response = self.get_response(request)
        return response
