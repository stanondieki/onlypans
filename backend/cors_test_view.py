from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json

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
