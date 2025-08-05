from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    CUISINE_CHOICES = [
        ('italian', 'Italian'),
        ('chinese', 'Chinese'),
        ('mexican', 'Mexican'),
        ('indian', 'Indian'),
        ('american', 'American'),
        ('french', 'French'),
        ('japanese', 'Japanese'),
        ('thai', 'Thai'),
        ('mediterranean', 'Mediterranean'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    servings = models.PositiveIntegerField(default=4)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    cuisine = models.CharField(max_length=20, choices=CUISINE_CHOICES, default='other')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    
    # Nutritional information
    calories_per_serving = models.PositiveIntegerField(null=True, blank=True)
    protein_grams = models.FloatField(null=True, blank=True)
    carbs_grams = models.FloatField(null=True, blank=True)
    fat_grams = models.FloatField(null=True, blank=True)
    fiber_grams = models.FloatField(null=True, blank=True)
    
    # AI generated fields
    ai_generated = models.BooleanField(default=False)
    source_image = models.ImageField(upload_to='ai_source/', blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    @property
    def total_time(self):
        return self.prep_time + self.cook_time
    
    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return 0


class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('cup', 'Cup'),
        ('tbsp', 'Tablespoon'),
        ('tsp', 'Teaspoon'),
        ('oz', 'Ounce'),
        ('lb', 'Pound'),
        ('g', 'Gram'),
        ('kg', 'Kilogram'),
        ('ml', 'Milliliter'),
        ('l', 'Liter'),
        ('piece', 'Piece'),
        ('slice', 'Slice'),
        ('clove', 'Clove'),
        ('bunch', 'Bunch'),
        ('can', 'Can'),
        ('package', 'Package'),
        ('to_taste', 'To taste'),
    ]
    
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    notes = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        
    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name}"


class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.PositiveIntegerField()
    instruction = models.TextField()
    time_minutes = models.PositiveIntegerField(null=True, blank=True, help_text="Time for this step in minutes")
    temperature = models.CharField(max_length=50, blank=True, help_text="Cooking temperature if applicable")
    
    class Meta:
        ordering = ['step_number']
        unique_together = ['recipe', 'step_number']
        
    def __str__(self):
        return f"Step {self.step_number}: {self.instruction[:50]}..."


class RecipeTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    recipes = models.ManyToManyField(Recipe, related_name='tags', blank=True)
    
    def __str__(self):
        return self.name


class RecipeRating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['recipe', 'user']
        
    def __str__(self):
        return f"{self.user.username} rated {self.recipe.title}: {self.rating}/5"


class RecipeFavorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['recipe', 'user']
        
    def __str__(self):
        return f"{self.user.username} favorited {self.recipe.title}"
