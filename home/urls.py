from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home/', views.home, name='home_page'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('join_us', views.join_us, name='join_us'),
    path('logout/', views.logout_view, name='logout'),
]
