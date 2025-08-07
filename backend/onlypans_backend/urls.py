"""
URL configuration for onlypans_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def health_check(request):
    """Health check endpoint for deployment platforms"""
    return JsonResponse({'status': 'healthy', 'message': 'OnlyPans backend is running'})

def simple_test(request):
    """Simple test endpoint"""
    response = JsonResponse({'message': 'Backend is working', 'cors': 'enabled'})
    response['Access-Control-Allow-Origin'] = '*'
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    path('api/test/', simple_test, name='simple_test'),
    path('api/auth/', include('accounts.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/meals/', include('meals.urls')),
    path('api/ai/', include('ai_assistant.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
