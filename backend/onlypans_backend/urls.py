"""
URL configuration for onlypans_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint for deployment platforms"""
    return JsonResponse({'status': 'healthy', 'message': 'OnlyPans backend is running'})

# Import the CORS test view
import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from cors_test_view import cors_test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    path('api/cors-test/', cors_test, name='cors_test'),
    path('api/auth/', include('accounts.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/meals/', include('meals.urls')),
    path('api/ai/', include('ai_assistant.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
