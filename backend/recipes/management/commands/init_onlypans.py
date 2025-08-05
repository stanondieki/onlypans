from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient, Instruction, RecipeTag
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Initialize OnlyPans with essential data for production use'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear_existing']:
            self.stdout.write(
                self.style.WARNING('Clearing existing data...')
            )
            Recipe.objects.all().delete()
            RecipeTag.objects.all().delete()
            
        self.stdout.write(
            self.style.HTTP_INFO('Initializing OnlyPans production data...')
        )

        # Create essential recipe tags
        self.create_recipe_tags()
        
        # Create starter recipes
        self.create_starter_recipes()
        
        self.stdout.write(
            self.style.SUCCESS('✅ OnlyPans initialization completed successfully!')
        )

    def create_recipe_tags(self):
        """Create essential recipe tags"""
        essential_tags = [
            # Meal types
            'breakfast', 'lunch', 'dinner', 'snack', 'dessert', 'brunch',
            
            # Dietary preferences
            'vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'keto', 
            'low-carb', 'high-protein', 'paleo', 'mediterranean',
            
            # Cooking styles
            'quick', 'easy', 'one-pot', 'no-cook', 'meal-prep', 'comfort-food',
            'healthy', 'light', 'hearty', 'spicy', 'sweet',
            
            # Cuisines
            'italian', 'chinese', 'mexican', 'indian', 'american', 'french',
            'japanese', 'thai', 'mediterranean', 'korean', 'greek',
            
            # Cooking methods
            'baked', 'grilled', 'fried', 'steamed', 'roasted', 'slow-cooked',
            'air-fried', 'instant-pot', 'microwave',
            
            # Occasions
            'family-friendly', 'date-night', 'party', 'holiday', 'weekend',
            'weeknight', 'budget-friendly', 'elegant'
        ]
        
        created_count = 0
        for tag_name in essential_tags:
            tag, created = RecipeTag.objects.get_or_create(name=tag_name)
            if created:
                created_count += 1
                
        self.stdout.write(f'✅ Created {created_count} recipe tags')

    def create_starter_recipes(self):
        """Create a collection of starter recipes"""
        
        # Get or create a system user for recipes
        system_user, created = User.objects.get_or_create(
            username='onlypans_system',
            defaults={
                'email': 'system@onlypans.com',
                'first_name': 'OnlyPans',
                'last_name': 'System',
                'is_active': False  # System user should not be able to login
            }
        )
        
        recipes_data = [
            {
                'title': 'Perfect Scrambled Eggs',
                'description': 'Creamy, fluffy scrambled eggs that are restaurant-quality every time',
                'prep_time': 5,
                'cook_time': 5,
                'servings': 2,
                'difficulty': 'easy',
                'cuisine': 'american',
                'calories_per_serving': 220,
                'protein_grams': 12,
                'carbs_grams': 2,
                'fat_grams': 18,
                'ingredients': [
                    {'name': 'Large eggs', 'quantity': 4, 'unit': 'piece', 'order': 1},
                    {'name': 'Butter', 'quantity': 2, 'unit': 'tbsp', 'order': 2},
                    {'name': 'Heavy cream', 'quantity': 2, 'unit': 'tbsp', 'order': 3},
                    {'name': 'Salt', 'quantity': 0.25, 'unit': 'tsp', 'order': 4},
                    {'name': 'Black pepper', 'quantity': 1, 'unit': 'to_taste', 'order': 5},
                    {'name': 'Fresh chives', 'quantity': 1, 'unit': 'tbsp', 'order': 6, 'notes': 'chopped, optional'},
                ],
                'instructions': [
                    {'step_number': 1, 'instruction': 'Crack eggs into a bowl and whisk with cream, salt, and pepper until well combined', 'time_minutes': 2},
                    {'step_number': 2, 'instruction': 'Heat butter in a non-stick pan over medium-low heat until melted and foamy', 'time_minutes': 1},
                    {'step_number': 3, 'instruction': 'Pour in egg mixture and let sit for 20 seconds without stirring', 'time_minutes': 1},
                    {'step_number': 4, 'instruction': 'Using a rubber spatula, gently stir from the edges toward center, creating soft curds', 'time_minutes': 2},
                    {'step_number': 5, 'instruction': 'Remove from heat while still slightly wet (they will continue cooking)', 'time_minutes': 1},
                    {'step_number': 6, 'instruction': 'Garnish with fresh chives if desired and serve immediately', 'time_minutes': 1},
                ],
                'tags': ['breakfast', 'quick', 'easy', 'vegetarian', 'high-protein', 'weeknight']
            },
            
            {
                'title': 'One-Pot Chicken and Rice',
                'description': 'Complete comfort meal with tender chicken, perfectly cooked rice, and vegetables',
                'prep_time': 15,
                'cook_time': 30,
                'servings': 4,
                'difficulty': 'easy',
                'cuisine': 'american',
                'calories_per_serving': 420,
                'protein_grams': 35,
                'carbs_grams': 45,
                'fat_grams': 12,
                'ingredients': [
                    {'name': 'Chicken thighs', 'quantity': 4, 'unit': 'piece', 'order': 1, 'notes': 'bone-in, skin-on'},
                    {'name': 'Long grain white rice', 'quantity': 1.5, 'unit': 'cup', 'order': 2},
                    {'name': 'Chicken broth', 'quantity': 2.5, 'unit': 'cup', 'order': 3},
                    {'name': 'Yellow onion', 'quantity': 1, 'unit': 'piece', 'order': 4, 'notes': 'diced'},
                    {'name': 'Carrots', 'quantity': 2, 'unit': 'piece', 'order': 5, 'notes': 'sliced'},
                    {'name': 'Frozen peas', 'quantity': 1, 'unit': 'cup', 'order': 6},
                    {'name': 'Garlic', 'quantity': 3, 'unit': 'clove', 'order': 7, 'notes': 'minced'},
                    {'name': 'Olive oil', 'quantity': 2, 'unit': 'tbsp', 'order': 8},
                    {'name': 'Salt', 'quantity': 1, 'unit': 'tsp', 'order': 9},
                    {'name': 'Black pepper', 'quantity': 0.5, 'unit': 'tsp', 'order': 10},
                    {'name': 'Paprika', 'quantity': 1, 'unit': 'tsp', 'order': 11},
                ],
                'instructions': [
                    {'step_number': 1, 'instruction': 'Season chicken thighs with salt, pepper, and paprika on both sides', 'time_minutes': 3},
                    {'step_number': 2, 'instruction': 'Heat olive oil in a large oven-safe pot over medium-high heat', 'time_minutes': 2},
                    {'step_number': 3, 'instruction': 'Brown chicken thighs skin-side down for 5 minutes, then flip and cook 3 more minutes', 'time_minutes': 8},
                    {'step_number': 4, 'instruction': 'Remove chicken and set aside. Add onion and carrots to the same pot', 'time_minutes': 3},
                    {'step_number': 5, 'instruction': 'Cook vegetables for 3-4 minutes until softened, then add garlic for 1 minute', 'time_minutes': 4},
                    {'step_number': 6, 'instruction': 'Add rice and stir for 1 minute to toast lightly', 'time_minutes': 1},
                    {'step_number': 7, 'instruction': 'Pour in chicken broth and bring to a boil', 'time_minutes': 3},
                    {'step_number': 8, 'instruction': 'Return chicken to pot, reduce heat to low, cover and simmer for 18 minutes', 'time_minutes': 18},
                    {'step_number': 9, 'instruction': 'Stir in frozen peas, cover and let rest off heat for 5 minutes before serving', 'time_minutes': 5},
                ],
                'tags': ['dinner', 'one-pot', 'family-friendly', 'comfort-food', 'hearty', 'easy', 'meal-prep']
            },
            
            {
                'title': 'Mediterranean Quinoa Bowl',
                'description': 'Fresh, healthy bowl packed with quinoa, vegetables, and Mediterranean flavors',
                'prep_time': 20,
                'cook_time': 15,
                'servings': 4,
                'difficulty': 'easy',
                'cuisine': 'mediterranean',
                'calories_per_serving': 320,
                'protein_grams': 12,
                'carbs_grams': 42,
                'fat_grams': 14,
                'ingredients': [
                    {'name': 'Quinoa', 'quantity': 1, 'unit': 'cup', 'order': 1, 'notes': 'rinsed'},
                    {'name': 'Vegetable broth', 'quantity': 2, 'unit': 'cup', 'order': 2},
                    {'name': 'Cherry tomatoes', 'quantity': 1, 'unit': 'cup', 'order': 3, 'notes': 'halved'},
                    {'name': 'Cucumber', 'quantity': 1, 'unit': 'piece', 'order': 4, 'notes': 'diced'},
                    {'name': 'Red onion', 'quantity': 0.25, 'unit': 'cup', 'order': 5, 'notes': 'finely diced'},
                    {'name': 'Kalamata olives', 'quantity': 0.5, 'unit': 'cup', 'order': 6, 'notes': 'pitted'},
                    {'name': 'Feta cheese', 'quantity': 0.5, 'unit': 'cup', 'order': 7, 'notes': 'crumbled'},
                    {'name': 'Fresh parsley', 'quantity': 0.25, 'unit': 'cup', 'order': 8, 'notes': 'chopped'},
                    {'name': 'Extra virgin olive oil', 'quantity': 3, 'unit': 'tbsp', 'order': 9},
                    {'name': 'Lemon juice', 'quantity': 2, 'unit': 'tbsp', 'order': 10, 'notes': 'fresh'},
                    {'name': 'Dried oregano', 'quantity': 1, 'unit': 'tsp', 'order': 11},
                ],
                'instructions': [
                    {'step_number': 1, 'instruction': 'Rinse quinoa in cold water until water runs clear', 'time_minutes': 2},
                    {'step_number': 2, 'instruction': 'Bring vegetable broth to boil, add quinoa, reduce heat and simmer covered for 15 minutes', 'time_minutes': 15},
                    {'step_number': 3, 'instruction': 'Remove quinoa from heat and let stand 5 minutes, then fluff with fork and cool', 'time_minutes': 10},
                    {'step_number': 4, 'instruction': 'While quinoa cools, prepare vegetables: halve tomatoes, dice cucumber and onion', 'time_minutes': 8},
                    {'step_number': 5, 'instruction': 'In a small bowl, whisk together olive oil, lemon juice, and oregano for dressing', 'time_minutes': 2},
                    {'step_number': 6, 'instruction': 'Combine cooled quinoa with vegetables, olives, and parsley in large bowl', 'time_minutes': 3},
                    {'step_number': 7, 'instruction': 'Drizzle with dressing and toss gently, then top with crumbled feta', 'time_minutes': 2},
                ],
                'tags': ['lunch', 'dinner', 'healthy', 'vegetarian', 'mediterranean', 'meal-prep', 'light', 'gluten-free']
            },
            
            {
                'title': '15-Minute Garlic Shrimp Pasta',
                'description': 'Quick and elegant pasta dish with succulent shrimp in garlic butter sauce',
                'prep_time': 5,
                'cook_time': 10,
                'servings': 4,
                'difficulty': 'medium',
                'cuisine': 'italian',
                'calories_per_serving': 480,
                'protein_grams': 28,
                'carbs_grams': 55,
                'fat_grams': 16,
                'ingredients': [
                    {'name': 'Linguine pasta', 'quantity': 12, 'unit': 'oz', 'order': 1},
                    {'name': 'Large shrimp', 'quantity': 1, 'unit': 'lb', 'order': 2, 'notes': 'peeled and deveined'},
                    {'name': 'Garlic', 'quantity': 4, 'unit': 'clove', 'order': 3, 'notes': 'minced'},
                    {'name': 'Butter', 'quantity': 4, 'unit': 'tbsp', 'order': 4},
                    {'name': 'Olive oil', 'quantity': 2, 'unit': 'tbsp', 'order': 5},
                    {'name': 'White wine', 'quantity': 0.5, 'unit': 'cup', 'order': 6, 'notes': 'optional'},
                    {'name': 'Lemon juice', 'quantity': 2, 'unit': 'tbsp', 'order': 7, 'notes': 'fresh'},
                    {'name': 'Red pepper flakes', 'quantity': 0.25, 'unit': 'tsp', 'order': 8},
                    {'name': 'Fresh parsley', 'quantity': 0.25, 'unit': 'cup', 'order': 9, 'notes': 'chopped'},
                    {'name': 'Parmesan cheese', 'quantity': 0.5, 'unit': 'cup', 'order': 10, 'notes': 'grated'},
                ],
                'instructions': [
                    {'step_number': 1, 'instruction': 'Bring large pot of salted water to boil and cook pasta according to package directions', 'time_minutes': 8},
                    {'step_number': 2, 'instruction': 'Pat shrimp dry and season with salt and pepper', 'time_minutes': 2},
                    {'step_number': 3, 'instruction': 'Heat olive oil and 2 tbsp butter in large skillet over medium-high heat', 'time_minutes': 1},
                    {'step_number': 4, 'instruction': 'Add shrimp and cook 1-2 minutes per side until pink, then remove to plate', 'time_minutes': 3},
                    {'step_number': 5, 'instruction': 'Add garlic and red pepper flakes to same pan, cook for 30 seconds until fragrant', 'time_minutes': 1},
                    {'step_number': 6, 'instruction': 'Add wine (if using) and lemon juice, simmer for 1 minute', 'time_minutes': 1},
                    {'step_number': 7, 'instruction': 'Add drained pasta and remaining butter, toss to combine', 'time_minutes': 1},
                    {'step_number': 8, 'instruction': 'Return shrimp to pan, add parsley and Parmesan, toss and serve immediately', 'time_minutes': 1},
                ],
                'tags': ['dinner', 'quick', 'italian', 'elegant', 'date-night', 'high-protein', 'weeknight']
            },
            
            {
                'title': 'Classic Chocolate Chip Cookies',
                'description': 'Perfectly chewy and crispy chocolate chip cookies that everyone will love',
                'prep_time': 15,
                'cook_time': 12,
                'servings': 24,
                'difficulty': 'easy',
                'cuisine': 'american',
                'calories_per_serving': 180,
                'protein_grams': 2,
                'carbs_grams': 24,
                'fat_grams': 9,
                'ingredients': [
                    {'name': 'All-purpose flour', 'quantity': 2.25, 'unit': 'cup', 'order': 1},
                    {'name': 'Baking soda', 'quantity': 1, 'unit': 'tsp', 'order': 2},
                    {'name': 'Salt', 'quantity': 1, 'unit': 'tsp', 'order': 3},
                    {'name': 'Butter', 'quantity': 1, 'unit': 'cup', 'order': 4, 'notes': 'softened'},
                    {'name': 'Granulated sugar', 'quantity': 0.75, 'unit': 'cup', 'order': 5},
                    {'name': 'Brown sugar', 'quantity': 0.75, 'unit': 'cup', 'order': 6, 'notes': 'packed'},
                    {'name': 'Large eggs', 'quantity': 2, 'unit': 'piece', 'order': 7},
                    {'name': 'Vanilla extract', 'quantity': 2, 'unit': 'tsp', 'order': 8},
                    {'name': 'Chocolate chips', 'quantity': 2, 'unit': 'cup', 'order': 9},
                ],
                'instructions': [
                    {'step_number': 1, 'instruction': 'Preheat oven to 375°F (190°C) and line baking sheets with parchment paper', 'time_minutes': 5},
                    {'step_number': 2, 'instruction': 'In medium bowl, whisk together flour, baking soda, and salt', 'time_minutes': 2},
                    {'step_number': 3, 'instruction': 'In large bowl, cream together softened butter and both sugars until fluffy', 'time_minutes': 3},
                    {'step_number': 4, 'instruction': 'Beat in eggs one at a time, then add vanilla extract', 'time_minutes': 2},
                    {'step_number': 5, 'instruction': 'Gradually mix in flour mixture until just combined', 'time_minutes': 2},
                    {'step_number': 6, 'instruction': 'Fold in chocolate chips with wooden spoon or spatula', 'time_minutes': 1},
                    {'step_number': 7, 'instruction': 'Drop rounded tablespoons of dough onto prepared baking sheets, 2 inches apart', 'time_minutes': 5},
                    {'step_number': 8, 'instruction': 'Bake for 9-11 minutes until golden brown around edges', 'time_minutes': 10},
                    {'step_number': 9, 'instruction': 'Cool on baking sheet for 5 minutes before transferring to wire rack', 'time_minutes': 5},
                ],
                'tags': ['dessert', 'sweet', 'baked', 'family-friendly', 'easy', 'comfort-food', 'weekend']
            }
        ]
        
        created_count = 0
        for recipe_data in recipes_data:
            # Check if recipe already exists
            if Recipe.objects.filter(title=recipe_data['title']).exists():
                continue
                
            # Extract related data
            ingredients_data = recipe_data.pop('ingredients')
            instructions_data = recipe_data.pop('instructions')
            tags_data = recipe_data.pop('tags')
            
            # Create recipe
            recipe = Recipe.objects.create(
                created_by=system_user,
                **recipe_data
            )
            
            # Create ingredients
            for ingredient_data in ingredients_data:
                Ingredient.objects.create(
                    recipe=recipe,
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
                tag, _ = RecipeTag.objects.get_or_create(name=tag_name)
                recipe.tags.add(tag)
            
            created_count += 1
            
        self.stdout.write(f'✅ Created {created_count} starter recipes')
