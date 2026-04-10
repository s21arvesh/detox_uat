from django.shortcuts import redirect
from django.conf import settings

class CustomLoginRequiredMiddleware:
    def __init__(self, get_response):
        print("CustomLoginRequiredMiddleware initialized")
        self.get_response = get_response

    def __call__(self, request):
        print(f"=== MIDDLEWARE CALLED FOR: {request.path} ===")
        
        # TEMPORARY: Make all paths require authentication except login/signup
        public_paths = [
            '/login/',
            '/signup/',
            '/static/',
            '/media/',
            '/admin/',
        ]
        
        # Normalize path to handle trailing slashes
        path = request.path.rstrip('/')
        
        # Check if current path is public
        is_public = any(path.startswith(p.rstrip('/')) for p in public_paths)
        print(f"Is public path: {is_public}")
        print(f"Is authenticated: {request.session.get('is_authenticated')}")
        
        # Check if user is authenticated via custom session
        if not request.session.get('is_authenticated') and not is_public:
            print(f"Redirecting to login for path: {request.path}")
            # Redirect to login page with next parameter
            return redirect(f'/login/?next={request.path}')
        
        response = self.get_response(request)
        return response
