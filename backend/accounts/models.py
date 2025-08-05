from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    DIETARY_CHOICES = [
        ('none', 'No Restrictions'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('pescatarian', 'Pescatarian'),
        ('keto', 'Ketogenic'),
        ('paleo', 'Paleo'),
        ('gluten_free', 'Gluten Free'),
        ('dairy_free', 'Dairy Free'),
        ('low_carb', 'Low Carb'),
        ('low_fat', 'Low Fat'),
        ('diabetic', 'Diabetic Friendly'),
    ]
    
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('lightly_active', 'Lightly Active'),
        ('moderately_active', 'Moderately Active'),
        ('very_active', 'Very Active'),
        ('extra_active', 'Extra Active'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Dietary preferences
    dietary_restrictions = models.CharField(max_length=20, choices=DIETARY_CHOICES, default='none')
    allergies = models.TextField(blank=True, help_text="List any food allergies")
    favorite_cuisines = models.JSONField(default=list, blank=True)
    disliked_ingredients = models.TextField(blank=True)
      # Cooking preferences
    cooking_skill_level = models.CharField(max_length=15, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ], default='beginner')
    
    preferred_meal_time = models.JSONField(default=dict, blank=True)  # Store preferred times for meals
    
    # Health & fitness
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, default='moderately_active')
    weight_goal = models.CharField(max_length=15, choices=[
        ('maintain', 'Maintain Weight'),
        ('lose', 'Lose Weight'),
        ('gain', 'Gain Weight'),
    ], default='maintain')
    
    # App preferences
    notifications_enabled = models.BooleanField(default=True)
    meal_reminders = models.BooleanField(default=True)
    shopping_reminders = models.BooleanField(default=True)
    recipe_recommendations = models.BooleanField(default=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class UserPreference(models.Model):
    """Store user preferences for recipes and ingredients"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    preference_type = models.CharField(max_length=20, choices=[
        ('ingredient', 'Ingredient'),
        ('cuisine', 'Cuisine'),
        ('dish_type', 'Dish Type'),
        ('cooking_method', 'Cooking Method'),
    ])
    name = models.CharField(max_length=100)
    preference_score = models.FloatField(default=0.0)  # Positive for likes, negative for dislikes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'preference_type', 'name']
        
    def __str__(self):
        return f"{self.user.username} - {self.name}: {self.preference_score}"
