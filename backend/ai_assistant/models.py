from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe


class AIRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('image_recognition', 'Image Recognition'),
        ('recipe_generation', 'Recipe Generation'),
        ('ingredient_suggestion', 'Ingredient Suggestion'),
        ('meal_planning', 'Meal Planning'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_requests')
    request_type = models.CharField(max_length=25, choices=REQUEST_TYPE_CHOICES)
    input_text = models.TextField(blank=True)
    input_image = models.ImageField(upload_to='ai_requests/', blank=True, null=True)
    response_text = models.TextField()
    generated_recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True)  # Time in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.request_type} on {self.created_at.date()}"


class FoodRecognition(models.Model):
    ai_request = models.OneToOneField(AIRequest, on_delete=models.CASCADE, related_name='food_recognition')
    detected_foods = models.JSONField(default=list)  # List of detected food items with confidence scores
    confidence_score = models.FloatField()
    
    def __str__(self):
        return f"Food recognition for {self.ai_request.user.username}"


class RecipeGeneration(models.Model):
    ai_request = models.OneToOneField(AIRequest, on_delete=models.CASCADE, related_name='recipe_generation')
    ingredients_provided = models.TextField()
    dietary_restrictions = models.CharField(max_length=200, blank=True)
    cuisine_preference = models.CharField(max_length=50, blank=True)
    difficulty_preference = models.CharField(max_length=10, blank=True)
    time_constraint = models.PositiveIntegerField(null=True, blank=True)  # Max time in minutes
    
    def __str__(self):
        return f"Recipe generation for {self.ai_request.user.username}"


class AIFeedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('incorrect', 'Incorrect'),
        ('incomplete', 'Incomplete'),
    ]
    
    ai_request = models.ForeignKey(AIRequest, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=15, choices=FEEDBACK_TYPE_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['ai_request', 'user']
        
    def __str__(self):
        return f"{self.user.username} - {self.feedback_type} for AI request"
