from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime, timedelta

from .models import MealPlan, Meal, ShoppingList, ShoppingListItem, MealRating
from .serializers import (
    MealPlanSerializer, MealPlanDetailSerializer, MealSerializer,
    ShoppingListSerializer, ShoppingListItemSerializer, MealRatingSerializer
)
from recipes.models import Recipe


class MealPlanListCreateView(generics.ListCreateAPIView):
    """List user's meal plans or create a new one"""
    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        meal_plan = serializer.save(user=self.request.user)
        # Create associated shopping list
        ShoppingList.objects.create(meal_plan=meal_plan)


class MealPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a meal plan"""
    serializer_class = MealPlanDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user).prefetch_related('meals__recipe')


class MealListCreateView(generics.ListCreateAPIView):
    """List meals for a meal plan or create a new meal"""
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        meal_plan_id = self.kwargs.get('meal_plan_id')
        meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=self.request.user)
        return Meal.objects.filter(meal_plan=meal_plan).select_related('recipe')
    
    def perform_create(self, serializer):
        meal_plan_id = self.kwargs.get('meal_plan_id')
        meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=self.request.user)
        serializer.save(meal_plan=meal_plan)


class MealDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a meal"""
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Meal.objects.filter(meal_plan__user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_meal_completed(request, meal_id):
    """Mark a meal as completed"""
    meal = get_object_or_404(Meal, id=meal_id, meal_plan__user=request.user)
    
    if not meal.completed:
        meal.completed = True
        meal.completed_at = datetime.now()
        meal.save()
        
        return Response({'message': 'Meal marked as completed'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Meal already completed'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_shopping_list(request, meal_plan_id):
    """Generate shopping list from meal plan"""
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)
    
    # Get or create shopping list
    shopping_list, created = ShoppingList.objects.get_or_create(meal_plan=meal_plan)
    
    # Clear existing items
    shopping_list.items.all().delete()
    
    # Aggregate ingredients from all meals
    ingredient_totals = {}
    
    for meal in meal_plan.meals.all():
        for ingredient in meal.recipe.ingredients.all():
            key = (ingredient.name.lower(), ingredient.unit)
            if key in ingredient_totals:
                ingredient_totals[key]['quantity'] += ingredient.quantity * meal.servings
            else:
                ingredient_totals[key] = {
                    'name': ingredient.name,
                    'quantity': ingredient.quantity * meal.servings,
                    'unit': ingredient.unit,
                    'category': _categorize_ingredient(ingredient.name)
                }
    
    # Create shopping list items
    for ingredient_data in ingredient_totals.values():
        ShoppingListItem.objects.create(
            shopping_list=shopping_list,
            **ingredient_data
        )
    
    return Response({'message': 'Shopping list generated successfully'}, status=status.HTTP_200_OK)


def _categorize_ingredient(ingredient_name):
    """Categorize ingredient for shopping list organization"""
    ingredient_lower = ingredient_name.lower()
    
    # Define categories
    produce = ['tomato', 'onion', 'garlic', 'potato', 'carrot', 'celery', 'lettuce', 'spinach', 
               'bell pepper', 'cucumber', 'avocado', 'banana', 'apple', 'lemon', 'lime']
    
    meat_seafood = ['chicken', 'beef', 'pork', 'fish', 'salmon', 'shrimp', 'turkey', 'lamb']
    
    dairy = ['milk', 'cheese', 'butter', 'yogurt', 'cream', 'eggs']
    
    pantry = ['rice', 'pasta', 'flour', 'sugar', 'salt', 'pepper', 'oil', 'vinegar', 
              'soy sauce', 'garlic powder', 'onion powder']
    
    # Check categories
    for item in produce:
        if item in ingredient_lower:
            return 'Produce'
    
    for item in meat_seafood:
        if item in ingredient_lower:
            return 'Meat & Seafood'
    
    for item in dairy:
        if item in ingredient_lower:
            return 'Dairy & Eggs'
    
    for item in pantry:
        if item in ingredient_lower:
            return 'Pantry'
    
    return 'Other'


class ShoppingListView(generics.RetrieveAPIView):
    """Get shopping list for a meal plan"""
    serializer_class = ShoppingListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        meal_plan_id = self.kwargs.get('meal_plan_id')
        meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=self.request.user)
        shopping_list, created = ShoppingList.objects.get_or_create(meal_plan=meal_plan)
        return shopping_list


class ShoppingListItemView(generics.RetrieveUpdateDestroyAPIView):
    """Update or delete shopping list item"""
    serializer_class = ShoppingListItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ShoppingListItem.objects.filter(shopping_list__meal_plan__user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_shopping_item(request, item_id):
    """Toggle purchased status of shopping list item"""
    item = get_object_or_404(ShoppingListItem, id=item_id, 
                           shopping_list__meal_plan__user=request.user)
    
    item.purchased = not item.purchased
    item.save()
    
    return Response({
        'message': f'Item marked as {"purchased" if item.purchased else "not purchased"}',
        'purchased': item.purchased
    }, status=status.HTTP_200_OK)


class MealRatingListCreateView(generics.ListCreateAPIView):
    """List meal ratings or create a new rating"""
    serializer_class = MealRatingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MealRating.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meal_plan_stats(request, meal_plan_id):
    """Get statistics for a meal plan"""
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)
    
    meals = meal_plan.meals.all()
    total_meals = meals.count()
    completed_meals = meals.filter(completed=True).count()
    
    # Calculate nutrition totals
    total_calories = sum(
        (meal.recipe.calories_per_serving or 0) * meal.servings 
        for meal in meals if meal.recipe.calories_per_serving
    )
    
    stats = {
        'total_meals': total_meals,
        'completed_meals': completed_meals,
        'completion_rate': (completed_meals / total_meals * 100) if total_meals > 0 else 0,
        'total_calories': total_calories,
        'avg_calories_per_day': total_calories / 7 if total_calories > 0 else 0,
        'meal_types_distribution': {
            'breakfast': meals.filter(meal_type='breakfast').count(),
            'lunch': meals.filter(meal_type='lunch').count(),
            'dinner': meals.filter(meal_type='dinner').count(),
            'snack': meals.filter(meal_type='snack').count(),
        }
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meals_by_date_range(request):
    """Get meals for a specific date range across all active meal plans"""
    from django.utils.dateparse import parse_date
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date:
        return Response({'error': 'start_date parameter is required'}, status=400)
    
    try:
        start_date = parse_date(start_date)
        if not start_date:
            raise ValueError
    except ValueError:
        return Response({'error': 'Invalid start_date format. Use YYYY-MM-DD'}, status=400)
    
    # If no end_date provided, use start_date + 6 days (week view)
    if end_date:
        try:
            end_date = parse_date(end_date)
            if not end_date:
                raise ValueError
        except ValueError:
            return Response({'error': 'Invalid end_date format. Use YYYY-MM-DD'}, status=400)
    else:
        end_date = start_date + timedelta(days=6)
    
    # Get all active meal plans for the user that overlap with the date range
    meal_plans = MealPlan.objects.filter(
        user=request.user,
        is_active=True,
        start_date__lte=end_date,
        end_date__gte=start_date
    )
    
    # Get all meals within the date range from these meal plans
    meals = Meal.objects.filter(
        meal_plan__in=meal_plans,
        date__range=[start_date, end_date]
    ).select_related('recipe').order_by('date', 'meal_type')
    
    # Serialize meals with recipe details
    serialized_meals = []
    for meal in meals:
        meal_data = MealSerializer(meal).data
        serialized_meals.append(meal_data)
    
    return Response({
        'meals': serialized_meals,
        'date_range': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'meal_plans_count': meal_plans.count()
    })
