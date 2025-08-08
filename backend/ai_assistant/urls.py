from django.urls import path
from . import views

urlpatterns = [
    # AI Requests
    path('requests/', views.AIRequestListView.as_view(), name='ai-request-list'),
    path('requests/<int:pk>/', views.AIRequestDetailView.as_view(), name='ai-request-detail'),
    
    # AI Services
    path('recognize-food/', views.recognize_food_image, name='recognize-food'),
    path('generate-recipe/', views.generate_recipe, name='generate-recipe'),
    path('suggest-ingredients/', views.suggest_ingredients, name='suggest-ingredients'),
    
    # AI Feedback
    path('requests/<int:request_id>/feedback/', views.submit_feedback, name='submit-feedback'),
    
    # AI Status and Statistics
    path('status/', views.ai_service_status, name='ai-service-status'),
    path('stats/', views.user_ai_stats, name='user-ai-stats'),
]
