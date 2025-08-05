from rest_framework import serializers
from .models import Recipe, Ingredient, Instruction, RecipeTag, RecipeRating, RecipeFavorite
from django.contrib.auth.models import User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity', 'unit', 'notes', 'order']


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ['id', 'step_number', 'instruction', 'time_minutes', 'temperature']


class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeTag
        fields = ['id', 'name']


class RecipeRatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = RecipeRating
        fields = ['id', 'rating', 'review', 'user_name', 'created_at']
        read_only_fields = ['user', 'created_at']


class RecipeListSerializer(serializers.ModelSerializer):
    """Serializer for recipe list view (minimal data)"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_time = serializers.ReadOnlyField()
    tags = RecipeTagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'image', 'prep_time', 'cook_time', 
            'total_time', 'servings', 'difficulty', 'cuisine', 'created_by_name',
            'average_rating', 'tags', 'calories_per_serving', 'ai_generated',
            'created_at'
        ]


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Serializer for recipe detail view (full data)"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    instructions = InstructionSerializer(many=True, read_only=True)
    tags = RecipeTagSerializer(many=True, read_only=True)
    ratings = RecipeRatingSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_time = serializers.ReadOnlyField()
    is_favorited = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'image', 'prep_time', 'cook_time',
            'total_time', 'servings', 'difficulty', 'cuisine', 'created_by',
            'created_by_name', 'created_at', 'updated_at', 'is_public',
            'calories_per_serving', 'protein_grams', 'carbs_grams', 'fat_grams',
            'fiber_grams', 'ai_generated', 'source_image', 'ingredients',
            'instructions', 'tags', 'ratings', 'average_rating', 'is_favorited',
            'user_rating'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return RecipeFavorite.objects.filter(recipe=obj, user=request.user).exists()
        return False
    
    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                rating = RecipeRating.objects.get(recipe=obj, user=request.user)
                return RecipeRatingSerializer(rating).data
            except RecipeRating.DoesNotExist:
                return None
        return None


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating recipes"""
    ingredients = IngredientSerializer(many=True)
    instructions = InstructionSerializer(many=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'image', 'prep_time', 'cook_time',
            'servings', 'difficulty', 'cuisine', 'is_public',
            'calories_per_serving', 'protein_grams', 'carbs_grams', 'fat_grams',
            'fiber_grams', 'ingredients', 'instructions', 'tags'
        ]
    
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instructions_data = validated_data.pop('instructions')
        tags_data = validated_data.pop('tags', [])
        
        recipe = Recipe.objects.create(**validated_data)
        
        # Create ingredients
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        
        # Create instructions
        for instruction_data in instructions_data:
            Instruction.objects.create(recipe=recipe, **instruction_data)
        
        # Create or get tags
        for tag_name in tags_data:
            tag, created = RecipeTag.objects.get_or_create(name=tag_name.lower())
            recipe.tags.add(tag)
        
        return recipe
    
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        instructions_data = validated_data.pop('instructions', None)
        tags_data = validated_data.pop('tags', None)
        
        # Update recipe fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update ingredients
        if ingredients_data is not None:
            instance.ingredients.all().delete()
            for ingredient_data in ingredients_data:
                Ingredient.objects.create(recipe=instance, **ingredient_data)
        
        # Update instructions
        if instructions_data is not None:
            instance.instructions.all().delete()
            for instruction_data in instructions_data:
                Instruction.objects.create(recipe=instance, **instruction_data)
        
        # Update tags
        if tags_data is not None:
            instance.tags.clear()
            for tag_name in tags_data:
                tag, created = RecipeTag.objects.get_or_create(name=tag_name.lower())
                instance.tags.add(tag)
        
        return instance


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    recipe_title = serializers.CharField(source='recipe.title', read_only=True)
    recipe_image = serializers.ImageField(source='recipe.image', read_only=True)
    
    class Meta:
        model = RecipeFavorite
        fields = ['id', 'recipe', 'recipe_title', 'recipe_image', 'created_at']
        read_only_fields = ['user', 'created_at']
