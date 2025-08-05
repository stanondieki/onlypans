from django.urls import path
from . import views

urlpatterns = [
    # Recipe CRUD
    path('', views.RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('my-recipes/', views.MyRecipesView.as_view(), name='my-recipes'),
    
    # Recipe Ratings
    path('<int:recipe_id>/rate/', views.rate_recipe, name='rate-recipe'),
    
    # Recipe Favorites
    path('<int:recipe_id>/favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    
    # Recipe Tags
    path('tags/', views.RecipeTagsView.as_view(), name='recipe-tags'),
    
    # Recipe Statistics
    path('stats/', views.recipe_stats, name='recipe-stats'),
]
