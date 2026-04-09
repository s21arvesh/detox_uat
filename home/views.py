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

            # Temporary test login without database
            if username == 'venom@2021' and password == 'venom123':
                # Create session manually
                request.session['user_id'] = 1
                request.session['username'] = username
                request.session['is_authenticated'] = True
                request.session.save()
                
                return JsonResponse({'success': True, 'message': f'Welcome back, {username}!'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid username or password.'})
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
                        INSERT INTO users (user, password, favorite_game, experience_level, created_at)
                        VALUES (%s, %s, %s, %s, NOW())
                    """, [email, password, favorite_game, experience_level])
            except Exception as db_error:
                # Continue even if custom database fails
                pass
            return JsonResponse({'success': True, 'message': 'Account created successfully! Please sign in.'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Registration failed. Please try again.'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})