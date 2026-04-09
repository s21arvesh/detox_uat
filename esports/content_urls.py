from django.urls import path
from esports import views

urlpatterns = [
    path('', views.content_creation, name='content_creation'),
]
