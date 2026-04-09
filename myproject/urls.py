"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views as home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('esports/', include('esports.urls')),
    path('bgmi/', include('esports.bgmi_urls')),
    path('valorant/', include('esports.valorant_urls')),
    path('cod_m', include('esports.codm_urls')),
    path('content_creation', include('esports.content_urls')),
    path('logout', home.logout_view, name='logout'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
