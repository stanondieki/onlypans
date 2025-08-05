import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlypans_backend.settings')
django.setup()

from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient, Instruction, RecipeTag
from accounts.models import UserProfile

def create_sample_data():
    # Create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@onlypans.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print("Test user created")
    
    # Create recipe tags
    tags_data = [
        'breakfast', 'lunch', 'dinner', 'snack', 'healthy', 'quick', 'vegetarian', 
        'vegan', 'gluten-free', 'low-carb', 'high-protein', 'comfort-food'
    ]
    
    for tag_name in tags_data:
        tag, created = RecipeTag.objects.get_or_create(name=tag_name)
        if created:
            print(f"Created tag: {tag_name}")
    
    # Create sample recipes
    recipes_data = [
        {
            'title': 'Classic Pancakes',
            'description': 'Fluffy and delicious pancakes perfect for breakfast',
            'prep_time': 10,
            'cook_time': 15,
            'servings': 4,
            'difficulty': 'easy',
            'cuisine': 'american',
            'calories_per_serving': 250,
            'ingredients': [
                {'name': 'All-purpose flour', 'quantity': 2, 'unit': 'cup'},
                {'name': 'Sugar', 'quantity': 2, 'unit': 'tbsp'},
                {'name': 'Baking powder', 'quantity': 2, 'unit': 'tsp'},
                {'name': 'Salt', 'quantity': 0.5, 'unit': 'tsp'},
                {'name': 'Milk', 'quantity': 1.75, 'unit': 'cup'},
                {'name': 'Eggs', 'quantity': 2, 'unit': 'piece'},
                {'name': 'Butter', 'quantity': 4, 'unit': 'tbsp'},
            ],
            'instructions': [
                {'step_number': 1, 'instruction': 'Mix dry ingredients in a large bowl'},
                {'step_number': 2, 'instruction': 'Whisk together milk, eggs, and melted butter'},
                {'step_number': 3, 'instruction': 'Combine wet and dry ingredients until just mixed'},
                {'step_number': 4, 'instruction': 'Cook on heated griddle until bubbles form and edges look set'},
                {'step_number': 5, 'instruction': 'Flip and cook until golden brown'}
            ],
            'tags': ['breakfast', 'quick']
        },
        {
            'title': 'Mediterranean Quinoa Salad',
            'description': 'Fresh and healthy quinoa salad with Mediterranean flavors',
            'prep_time': 20,
            'cook_time': 15,
            'servings': 6,
            'difficulty': 'easy',
            'cuisine': 'mediterranean',
            'calories_per_serving': 180,
            'ingredients': [
                {'name': 'Quinoa', 'quantity': 1, 'unit': 'cup'},
                {'name': 'Cherry tomatoes', 'quantity': 1, 'unit': 'cup'},
                {'name': 'Cucumber', 'quantity': 1, 'unit': 'piece'},
                {'name': 'Red onion', 'quantity': 0.25, 'unit': 'cup'},
                {'name': 'Feta cheese', 'quantity': 0.5, 'unit': 'cup'},
                {'name': 'Olive oil', 'quantity': 3, 'unit': 'tbsp'},
                {'name': 'Lemon juice', 'quantity': 2, 'unit': 'tbsp'},
            ],
            'instructions': [
                {'step_number': 1, 'instruction': 'Cook quinoa according to package directions and let cool'},
                {'step_number': 2, 'instruction': 'Dice tomatoes, cucumber, and red onion'},
                {'step_number': 3, 'instruction': 'Combine quinoa with vegetables and feta cheese'},
                {'step_number': 4, 'instruction': 'Whisk olive oil and lemon juice for dressing'},
                {'step_number': 5, 'instruction': 'Toss salad with dressing and let marinate for 15 minutes'}
            ],
            'tags': ['healthy', 'vegetarian', 'lunch']
        }
    ]
    
    for recipe_data in recipes_data:
        # Check if recipe already exists
        if Recipe.objects.filter(title=recipe_data['title']).exists():
            print(f"Recipe '{recipe_data['title']}' already exists")
            continue
            
        # Create recipe
        ingredients_data = recipe_data.pop('ingredients')
        instructions_data = recipe_data.pop('instructions')
        tags_data = recipe_data.pop('tags')
        
        recipe = Recipe.objects.create(
            created_by=user,
            **recipe_data
        )
        
        # Create ingredients
        for i, ingredient_data in enumerate(ingredients_data):
            Ingredient.objects.create(
                recipe=recipe,
                order=i + 1,
                **ingredient_data
            )
        
        # Create instructions
        for instruction_data in instructions_data:
            Instruction.objects.create(
                recipe=recipe,
                **instruction_data
            )
        
        # Add tags
        for tag_name in tags_data:
            tag = RecipeTag.objects.get(name=tag_name)
            recipe.tags.add(tag)
        
        print(f"Created recipe: {recipe.title}")

if __name__ == '__main__':
    create_sample_data()
    print("Sample data creation completed!")
