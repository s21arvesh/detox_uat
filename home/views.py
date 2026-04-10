from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.db import connection

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    print(f"Home view called")
    print(f"Session data: {dict(request.session)}")
    print(f"Is authenticated: {request.session.get('is_authenticated')}")
    return render(request, 'home.html')

def join_us(request):
    return render(request, 'joinus.html')

def login_view(request):
    # Clear any existing messages to prevent accumulation
    messages.get_messages(request).used = True
    
    if request.method == 'POST':
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Single query to validate username and password
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id, user, password, first_name, last_name FROM users WHERE user = %s AND password = %s", [username, password])
                    user_data = cursor.fetchone()
                    
                    if user_data:
                        # User found and password matches - create session directly
                        user_id, db_username, db_password, first_name, last_name = user_data
                        
                        # Create session manually since we're using custom database
                        request.session['user_id'] = user_id
                        request.session['username'] = db_username
                        request.session['first_name'] = first_name
                        request.session['last_name'] = last_name
                        request.session['is_authenticated'] = True
                        request.session.save()
                        
                        display_name = first_name or db_username
                        return JsonResponse({'success': True, 'message': f'Welcome back, {display_name}!'})
                    else:
                        return JsonResponse({'success': False, 'error': 'Invalid username or password.'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': 'Authentication failed.'})
        else:
            # Traditional form submission (non-AJAX)
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Welcome back, {username}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    # Clear custom session
    request.session.flush()
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        # Get form data from AJAX request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        favorite_game = request.POST.get('favorite_game')
        experience_level = request.POST.get('experience_level')
        
                
        # Validate form data
        if not all([username, email, password, favorite_game, experience_level]):
            return JsonResponse({'success': False, 'error': 'All fields are required.'})
        
        if len(password) < 6:
            return JsonResponse({'success': False, 'error': 'Password must be at least 6 characters long.'})
        
        if '@' not in email:
            return JsonResponse({'success': False, 'error': 'Please enter a valid email address.'})
        
        try:
            # Check if username or email already exists in Django User model
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': 'Username already exists.'})
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'Email already exists.'})
            
            # Create new Django User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Store additional info in custom database if needed
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO users (user, password, first_name, last_name, favorite_game, experience_level, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW())
                    """, [email, password, username, '', favorite_game, experience_level])
            except Exception as db_error:
                # Continue even if custom database fails
                pass
            return JsonResponse({'success': True, 'message': 'Account created successfully! Please sign in.'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Registration failed. Please try again.'})
    
    # Handle GET request - display signup page
    return render(request, 'signup.html')