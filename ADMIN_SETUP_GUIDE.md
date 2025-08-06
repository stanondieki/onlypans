# Admin User Creation Guide for OnlyPans

## Step 1: Access Render Shell
1. Go to https://dashboard.render.com
2. Find the "onlypans" service
3. Click on it, then go to the "Shell" tab
4. Click "Launch Shell"

## Step 2: Create Admin User
In the Render shell, run these commands:

```bash
# Navigate to the app directory (if needed)
cd /app

# Create admin user
python manage.py createsuperuser

# Or use our custom command
python manage.py create_admin --username admin --email admin@onlypans.com --password admin123

# Or run the quick admin script
python create_quick_admin.py
```

## Step 3: Initialize Data (if needed)
```bash
# Initialize recipes and tags
python manage.py init_onlypans

# Check data was created
python manage.py shell -c "from recipes.models import Recipe; print(f'Recipes: {Recipe.objects.count()}')"
```

## Step 4: Test Login
Once admin user is created, test login at:
- Frontend: https://onlypans-ctfazewa7-stanondiekis-projects.vercel.app/login
- Backend Admin: https://onlypans.onrender.com/admin/

## Step 5: Create Meal Plan
After logging in:
1. Go to the meals page
2. If no meals show up, create a meal plan first
3. Add some meals to the plan
4. Then the meal schedule should work

## Troubleshooting

### Backend Cold Start
If the backend is slow to respond, it might be in cold start. Wait 30-60 seconds and try again.

### API Endpoint Test
Test the new meals by date API:
```
GET https://onlypans.onrender.com/api/meals/by-date/?start_date=2024-01-15
```

### Database Check
Check if data exists:
```bash
python manage.py shell -c "
from django.contrib.auth.models import User
from recipes.models import Recipe
from meals.models import MealPlan, Meal
print(f'Users: {User.objects.count()}')
print(f'Recipes: {Recipe.objects.count()}')
print(f'Meal Plans: {MealPlan.objects.count()}')
print(f'Meals: {Meal.objects.count()}')
"
```
