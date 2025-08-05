from rest_framework import serializers
from .models import AIRequest, FoodRecognition, RecipeGeneration, AIFeedback
from recipes.serializers import RecipeListSerializer


class FoodRecognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodRecognition
        fields = ['detected_foods', 'confidence_score']


class RecipeGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeGeneration
        fields = [
            'ingredients_provided', 'dietary_restrictions', 'cuisine_preference',
            'difficulty_preference', 'time_constraint'
        ]


class AIRequestSerializer(serializers.ModelSerializer):
    food_recognition = FoodRecognitionSerializer(read_only=True)
    recipe_generation = RecipeGenerationSerializer(read_only=True)
    generated_recipe_details = RecipeListSerializer(source='generated_recipe', read_only=True)
    
    class Meta:
        model = AIRequest
        fields = [
            'id', 'request_type', 'input_text', 'input_image', 'response_text',
            'generated_recipe', 'generated_recipe_details', 'processing_time', 
            'created_at', 'food_recognition', 'recipe_generation'
        ]
        read_only_fields = ['user', 'created_at', 'processing_time']


class AIRequestCreateSerializer(serializers.ModelSerializer):
    # Additional fields for recipe generation
    dietary_restrictions = serializers.CharField(required=False, allow_blank=True)
    cuisine_preference = serializers.CharField(required=False, allow_blank=True)
    difficulty_preference = serializers.CharField(required=False, allow_blank=True)
    time_constraint = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = AIRequest
        fields = [
            'request_type', 'input_text', 'input_image',
            'dietary_restrictions', 'cuisine_preference', 
            'difficulty_preference', 'time_constraint'
        ]
    
    def validate(self, data):
        request_type = data.get('request_type')
        
        if request_type == 'image_recognition' and not data.get('input_image'):
            raise serializers.ValidationError("Image is required for image recognition requests.")
        
        if request_type in ['recipe_generation', 'ingredient_suggestion'] and not data.get('input_text'):
            raise serializers.ValidationError("Text input is required for recipe generation requests.")
        
        return data


class AIFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIFeedback
        fields = ['id', 'ai_request', 'feedback_type', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']


class ImageRecognitionRequestSerializer(serializers.Serializer):
    """Simplified serializer for image recognition requests"""
    image = serializers.ImageField()
    
    def validate_image(self, value):
        # Validate image size (10MB max)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Image size cannot exceed 10MB.")
        
        # Validate image format
        allowed_formats = ['JPEG', 'JPG', 'PNG', 'WebP']
        if not any(value.name.upper().endswith(fmt) for fmt in allowed_formats):
            raise serializers.ValidationError("Only JPEG, PNG, and WebP images are allowed.")
        
        return value


class RecipeGenerationRequestSerializer(serializers.Serializer):
    """Simplified serializer for recipe generation requests"""
    ingredients = serializers.CharField(
        help_text="List of available ingredients, separated by commas"
    )
    dietary_restrictions = serializers.CharField(required=False, allow_blank=True)
    cuisine_preference = serializers.CharField(required=False, allow_blank=True)
    difficulty_preference = serializers.ChoiceField(
        choices=['easy', 'medium', 'hard'], 
        required=False
    )
    time_constraint = serializers.IntegerField(
        required=False, 
        min_value=5, 
        max_value=480,
        help_text="Maximum cooking time in minutes"
    )
    servings = serializers.IntegerField(
        required=False, 
        min_value=1, 
        max_value=12,
        default=4
    )


class AIResponseSerializer(serializers.Serializer):
    """Serializer for AI response data"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = serializers.JSONField(required=False)
    processing_time = serializers.FloatField(required=False)
    request_id = serializers.IntegerField(required=False)
