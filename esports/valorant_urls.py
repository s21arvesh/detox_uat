from django.urls import path
from esports import views

urlpatterns = [
    path('', views.valorant, name='valorant'),
]
