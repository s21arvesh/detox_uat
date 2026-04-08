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

def esports(request):
    return render(request, 'esports.html')

def join_us(request):
    return render(request, 'joinus.html')

def bgmi(request):
    return render(request, 'bgmi.html')

def valorant(request):
    return render(request, 'valorant.html')

def cod_m(request):
    return render(request, 'codm.html')

def login_view(request):
    if request.method == 'POST':
        # Check if this is an AJAX request
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            username = request.POST.get('username')
            password = request.POST.get('password')

            print(f"Username: {username}, Password: {password}")
            
            # Test database connection
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    print("MySQL database connection successful!")
                    
                    # Debug: Show all table structure
                    cursor.execute("DESCRIBE users")
                    columns = cursor.fetchall()
                    print("=== USERS TABLE COLUMNS ===")
                    for col in columns:
                        print(f"Column: {col[0]}")
                    print("========================")
            except Exception as e:
                print(f"MySQL connection error: {e}")
                return JsonResponse({'success': False, 'error': 'Database connection failed.'})
            
            # Check if the input is an email address
            if '@' in username:
                print(f"Email login attempt: {username}")
                # Single query to validate both email and password
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT id, user, password FROM users WHERE user = %s AND password = %s", [username, password])
                        columns = [col[0] for col in cursor.description]
                        row = cursor.fetchone()
                        user_data = dict(zip(columns, row)) if row else None
                        print(f"User dataaaa: {user_data}")
                        if user_data:
                            print(f"Retrieved username: {user_data['user']}")
                            # User found and password matches
                            # Authenticate with Django for session management
                            # user = authenticate(request, username=retrieved_username, password=password)
                            if user_data['password'] == password:
                                return JsonResponse({'success': True, 'message': f'Welcome back, {user_data["user"]}!'})
                            else:
                                return JsonResponse({'success': False, 'error': 'Authentication failed.'})
                        else:
                            return JsonResponse({'success': False, 'error': 'Invalid email or password.'})
                except Exception as e:
                    print(f"Database query error: {e}")
                    return JsonResponse({'success': False, 'error': 'Database query failed.'})
            else:
                print(f"Username login attempt: {username}")
                # Single query to validate both username and password
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT id, user, password FROM users WHERE user = %s AND password = %s", [username, password])
                        user_data = cursor.fetchone()
                        if user_data:
                            # User found and password matches
                            user = authenticate(request, username=username, password=password)
                            print(f"Django authenticate result: {user}")
                            print(f"Username used for auth: {username}")
                            print(f"Password used for auth: {password}")
                            if user is not None:
                                login(request, user)
                                print("Django login successful!")
                                return JsonResponse({'success': True, 'message': f'Welcome back, {username}!'})
                            else:
                                print("Django authentication failed - checking password hash...")
                                # Debug: Check if password exists in database
                                with connection.cursor() as cursor:
                                    cursor.execute("SELECT password FROM users WHERE user = %s", [username])
                                    db_password = cursor.fetchone()
                                    print(f"Database password: {db_password}")
                                return JsonResponse({'success': False, 'error': 'Authentication failed.'})
                        else:
                            return JsonResponse({'success': False, 'error': 'Invalid username or password.'})
                except Exception as e:
                    print(f"Database query error: {e}")
                    return JsonResponse({'success': False, 'error': 'Database query failed.'})
        else:
            # Traditional form submission (non-AJAX)
            form = AuthenticationForm(request, data=request.POST)
            print(form)
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
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        # Get form data from AJAX request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        favorite_game = request.POST.get('favorite_game')
        experience_level = request.POST.get('experience_level')
        
        print(f"Signup attempt - Username: {username}, Email: {email}, Game: {favorite_game}, Experience: {experience_level}")
        
        # Validate form data
        if not all([username, email, password, favorite_game, experience_level]):
            return JsonResponse({'success': False, 'error': 'All fields are required.'})
        
        if len(password) < 6:
            return JsonResponse({'success': False, 'error': 'Password must be at least 6 characters long.'})
        
        if '@' not in email:
            return JsonResponse({'success': False, 'error': 'Please enter a valid email address.'})
        
        try:
            with connection.cursor() as cursor:
                # Check if username or email already exists
                cursor.execute("SELECT id FROM users WHERE user = %s OR user = %s", [username, email])
                if cursor.fetchone():
                    return JsonResponse({'success': False, 'error': 'Username or email already exists.'})
                
                # Insert new user
                cursor.execute("""
                    INSERT INTO users (user, password, favorite_game, experience_level, created_at)
                    VALUES (%s, %s, %s, %s, NOW())
                """, [email, password, favorite_game, experience_level])
                
                print(f"New user created: {username}")
                return JsonResponse({'success': True, 'message': 'Account created successfully! Please sign in.'})
                
        except Exception as e:
            print(f"Database error during signup: {e}")
            return JsonResponse({'success': False, 'error': 'Registration failed. Please try again.'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})