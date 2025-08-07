from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import UserProfile, UserPreference
from .serializers import (
    UserSerializer, UserProfileSerializer, UserProfileDetailSerializer,
    UserPreferenceSerializer, UserRegistrationSerializer, UserUpdateSerializer,
    PasswordChangeSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """Register a new user"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view with additional user data"""
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get user data
            from rest_framework_simplejwt.tokens import UntypedToken
            from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
            import jwt
            from django.conf import settings
            
            try:
                token = response.data['access']
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token['user_id']
                user = User.objects.get(id=user_id)
                
                user_serializer = UserSerializer(user)
                profile_serializer = UserProfileSerializer(user.userprofile)
                
                response.data['user'] = user_serializer.data
                response.data['profile'] = profile_serializer.data
                
            except (InvalidToken, TokenError, User.DoesNotExist):
                pass
        
        return response


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get or update user profile"""
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.userprofile


class UserUpdateView(generics.UpdateAPIView):
    """Update user information"""
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user password"""
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPreferenceListCreateView(generics.ListCreateAPIView):
    """List or create user preferences"""
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPreferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete a user preference"""
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_preference_score(request, preference_id):
    """Update preference score for a specific preference"""
    preference = get_object_or_404(UserPreference, id=preference_id, user=request.user)
    
    score = request.data.get('score')
    if score is not None:
        try:
            score = float(score)
            preference.preference_score = score
            preference.save()
            
            return Response({
                'message': 'Preference score updated successfully',
                'preference': UserPreferenceSerializer(preference).data
            }, status=status.HTTP_200_OK)
        except ValueError:
            return Response({
                'error': 'Invalid score value'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'error': 'Score is required'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_statistics(request):
    """Get user statistics"""
    user = request.user
    
    # Import here to avoid circular imports
    from recipes.models import Recipe, RecipeRating, RecipeFavorite
    from meals.models import MealPlan, Meal
    from ai_assistant.models import AIRequest
    
    stats = {
        'recipes_created': Recipe.objects.filter(created_by=user).count(),
        'recipes_rated': RecipeRating.objects.filter(user=user).count(),
        'recipes_favorited': RecipeFavorite.objects.filter(user=user).count(),
        'meal_plans_created': MealPlan.objects.filter(user=user).count(),
        'meals_completed': Meal.objects.filter(meal_plan__user=user, completed=True).count(),
        'ai_requests_made': AIRequest.objects.filter(user=user).count(),
        'ai_recipes_generated': AIRequest.objects.filter(
            user=user, 
            request_type='recipe_generation',
            generated_recipe__isnull=False
        ).count(),
        'member_since': user.date_joined,
        'profile_completion': _calculate_profile_completion(user.userprofile)
    }
    
    return Response(stats)


def _calculate_profile_completion(profile):
    """Calculate profile completion percentage"""
    fields_to_check = [
        'bio', 'avatar', 'date_of_birth', 'dietary_restrictions',
        'cooking_skill_level', 'activity_level', 'weight_goal'
    ]
    
    completed_fields = 0
    total_fields = len(fields_to_check)
    
    for field in fields_to_check:
        value = getattr(profile, field, None)
        if value:
            if field == 'avatar' and hasattr(value, 'name') and value.name:
                completed_fields += 1
            elif field != 'avatar' and value:
                completed_fields += 1
    
    return round((completed_fields / total_fields) * 100, 1)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """Delete user account"""
    password = request.data.get('password')
    
    if not password:
        return Response({
            'error': 'Password is required to delete account'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    if not user.check_password(password):
        return Response({
            'error': 'Incorrect password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete user account (this will cascade to related objects)
    user.delete()
    
    return Response({
        'message': 'Account deleted successfully'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    """Get dashboard data for user"""
    user = request.user
    
    # Import here to avoid circular imports
    from recipes.models import Recipe
    from meals.models import MealPlan, Meal
    from ai_assistant.models import AIRequest
    from datetime import datetime, timedelta
    
    # Get recent activity
    recent_recipes = Recipe.objects.filter(created_by=user).order_by('-created_at')[:5]
    active_meal_plans = MealPlan.objects.filter(user=user, is_active=True).order_by('-created_at')[:3]
    recent_ai_requests = AIRequest.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Get upcoming meals
    today = datetime.now().date()
    upcoming_meals = Meal.objects.filter(
        meal_plan__user=user,
        date__gte=today,
        completed=False
    ).order_by('date', 'meal_type')[:10]
    
    dashboard_data = {
        'recent_recipes': [
            {
                'id': recipe.id,
                'title': recipe.title,
                'difficulty': recipe.difficulty,
                'created_at': recipe.created_at
            } for recipe in recent_recipes
        ],
        'active_meal_plans': [
            {
                'id': plan.id,
                'name': plan.name,
                'start_date': plan.start_date,
                'end_date': plan.end_date,
                'meals_count': plan.meals.count()
            } for plan in active_meal_plans
        ],
        'upcoming_meals': [
            {
                'id': meal.id,
                'recipe_title': meal.recipe.title,
                'date': meal.date,
                'meal_type': meal.meal_type,
                'servings': meal.servings
            } for meal in upcoming_meals
        ],
        'recent_ai_activity': [
            {
                'id': request.id,
                'request_type': request.request_type,
                'created_at': request.created_at,
                'success': bool(request.response_text and 'error' not in request.response_text.lower())
            } for request in recent_ai_requests
        ]
    }
    
    return Response(dashboard_data)
