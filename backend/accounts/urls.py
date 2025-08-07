from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # User Profile
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('update/', views.UserUpdateView.as_view(), name='user-update'),
    path('change-password/', views.change_password, name='change-password'),
    path('delete-account/', views.delete_account, name='delete-account'),
    
    # User Preferences
    path('preferences/', views.UserPreferenceListCreateView.as_view(), name='user-preferences'),
    path('preferences/<int:pk>/', views.UserPreferenceDetailView.as_view(), name='user-preference-detail'),
    path('preferences/<int:preference_id>/score/', views.update_preference_score, name='update-preference-score'),
    
    # User Statistics and Dashboard
    path('stats/', views.user_statistics, name='user-statistics'),
    path('dashboard/', views.user_dashboard, name='user-dashboard'),
]
