from rest_framework import serializers
from .models import MealPlan, Meal, ShoppingList, ShoppingListItem, MealRating
from recipes.serializers import RecipeListSerializer


class MealPlanSerializer(serializers.ModelSerializer):
    meals_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MealPlan
        fields = [
            'id', 'name', 'start_date', 'end_date', 'created_at', 
            'updated_at', 'is_active', 'meals_count'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_meals_count(self, obj):
        return obj.meals.count()


class MealSerializer(serializers.ModelSerializer):
    recipe_details = RecipeListSerializer(source='recipe', read_only=True)
    
    class Meta:
        model = Meal
        fields = [
            'id', 'recipe', 'recipe_details', 'date', 'meal_type', 
            'servings', 'notes', 'completed', 'completed_at', 'created_at'
        ]
        read_only_fields = ['meal_plan', 'created_at', 'completed_at']


class MealPlanDetailSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, read_only=True)
    meals_by_date = serializers.SerializerMethodField()
    
    class Meta:
        model = MealPlan
        fields = [
            'id', 'name', 'start_date', 'end_date', 'created_at', 
            'updated_at', 'is_active', 'meals', 'meals_by_date'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_meals_by_date(self, obj):
        meals = obj.meals.all().order_by('date', 'meal_type')
        meals_dict = {}
        
        for meal in meals:
            date_str = meal.date.isoformat()
            if date_str not in meals_dict:
                meals_dict[date_str] = {
                    'breakfast': None,
                    'lunch': None,
                    'dinner': None,
                    'snack': None
                }
            meals_dict[date_str][meal.meal_type] = MealSerializer(meal).data
        
        return meals_dict


class ShoppingListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListItem
        fields = [
            'id', 'ingredient_name', 'quantity', 'unit', 'category',
            'purchased', 'notes', 'created_at'
        ]
        read_only_fields = ['shopping_list', 'created_at']


class ShoppingListSerializer(serializers.ModelSerializer):
    items = ShoppingListItemSerializer(many=True, read_only=True)
    items_by_category = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    purchased_items = serializers.SerializerMethodField()
    
    class Meta:
        model = ShoppingList
        fields = [
            'id', 'created_at', 'updated_at', 'items', 'items_by_category',
            'total_items', 'purchased_items'
        ]
        read_only_fields = ['meal_plan', 'created_at', 'updated_at']
    
    def get_items_by_category(self, obj):
        items = obj.items.all().order_by('category', 'ingredient_name')
        categories = {}
        
        for item in items:
            category = item.category or 'Other'
            if category not in categories:
                categories[category] = []
            categories[category].append(ShoppingListItemSerializer(item).data)
        
        return categories
    
    def get_total_items(self, obj):
        return obj.items.count()
    
    def get_purchased_items(self, obj):
        return obj.items.filter(purchased=True).count()


class MealRatingSerializer(serializers.ModelSerializer):
    meal_details = serializers.SerializerMethodField()
    
    class Meta:
        model = MealRating
        fields = [
            'id', 'meal', 'meal_details', 'rating', 'notes', 
            'would_make_again', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']
    
    def get_meal_details(self, obj):
        return {
            'date': obj.meal.date,
            'meal_type': obj.meal.meal_type,
            'recipe_title': obj.meal.recipe.title
        }
