from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home/', views.home, name='home_page'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    # path('esports', views.esports, name='esports'),
    path('join_us', views.join_us, name='join_us'),
    # path('bgmi', views.bgmi, name='bgmi'),
    path('valorant', views.valorant, name='valorant'),
    path('cod_m', views.cod_m, name='cod_m')
]
