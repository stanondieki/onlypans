from django.urls import path
from . import views

urlpatterns = [
    # Meal Plans
    path('plans/', views.MealPlanListCreateView.as_view(), name='meal-plan-list-create'),
    path('plans/<int:pk>/', views.MealPlanDetailView.as_view(), name='meal-plan-detail'),
    path('plans/<int:meal_plan_id>/stats/', views.meal_plan_stats, name='meal-plan-stats'),
    
    # Meals
    path('plans/<int:meal_plan_id>/meals/', views.MealListCreateView.as_view(), name='meal-list-create'),
    path('meals/<int:pk>/', views.MealDetailView.as_view(), name='meal-detail'),
    path('meals/<int:meal_id>/complete/', views.mark_meal_completed, name='mark-meal-completed'),
    
    # Shopping Lists
    path('plans/<int:meal_plan_id>/shopping-list/', views.ShoppingListView.as_view(), name='shopping-list'),
    path('plans/<int:meal_plan_id>/generate-shopping-list/', views.generate_shopping_list, name='generate-shopping-list'),
    path('shopping-items/<int:pk>/', views.ShoppingListItemView.as_view(), name='shopping-list-item'),
    path('shopping-items/<int:item_id>/toggle/', views.toggle_shopping_item, name='toggle-shopping-item'),
    
    # Meal Ratings
    path('ratings/', views.MealRatingListCreateView.as_view(), name='meal-rating-list-create'),
]
