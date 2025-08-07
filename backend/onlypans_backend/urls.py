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

@csrf_exempt
@require_http_methods(["GET", "POST", "OPTIONS"])
def cors_test(request):
    """Simple endpoint to test CORS configuration"""
    
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = JsonResponse({'message': 'CORS preflight successful'})
    else:
        # Return CORS configuration info
        response = JsonResponse({
            'message': 'CORS test endpoint',
            'method': request.method,
            'origin': request.META.get('HTTP_ORIGIN', 'None'),
            'cors_settings': {
                'CORS_ALLOW_ALL_ORIGINS': getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', None),
                'CORS_ALLOWED_ORIGINS': getattr(settings, 'CORS_ALLOWED_ORIGINS', None),
                'CORS_ALLOW_CREDENTIALS': getattr(settings, 'CORS_ALLOW_CREDENTIALS', None),
            }
        })
    
    return response

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
