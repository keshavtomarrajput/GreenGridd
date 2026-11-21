"""
URL Configuration for GreenGrid Backend
"""

from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.web_dashboard, name='home'),
    path('dashboard/', views.web_dashboard, name='dashboard'),
    path('api-info/', views.api_root_view, name='api-info'),
    path('api/', include('core.urls')),
]
