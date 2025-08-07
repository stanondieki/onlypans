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

def cors_debug(request):
    """Simple CORS debug endpoint"""
    from django.conf import settings
    
    response_data = {
        'cors_debug': True,
        'method': request.method,
        'origin': request.META.get('HTTP_ORIGIN', 'No origin header'),
        'cors_allow_all_origins': getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', 'Not set'),
        'cors_allowed_origins': getattr(settings, 'CORS_ALLOWED_ORIGINS', 'Not set'),
        'cors_allow_credentials': getattr(settings, 'CORS_ALLOW_CREDENTIALS', 'Not set'),
    }
    
    response = JsonResponse(response_data)
    
    # Manually add CORS headers as a backup
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization, X-Requested-With'
    response['Access-Control-Allow-Credentials'] = 'true'
    
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    path('api/cors-test/', cors_debug, name='cors_debug'),
    path('api/auth/', include('accounts.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/meals/', include('meals.urls')),
    path('api/ai/', include('ai_assistant.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
