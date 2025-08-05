from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count
from django.shortcuts import get_object_or_404
from django.db import models

from .models import Recipe, RecipeRating, RecipeFavorite, RecipeTag
from .serializers import (
    RecipeListSerializer, RecipeDetailSerializer, RecipeCreateUpdateSerializer,
    RecipeRatingSerializer, RecipeFavoriteSerializer, RecipeTagSerializer
)


class RecipeListCreateView(generics.ListCreateAPIView):
    """List all recipes or create a new recipe"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty', 'cuisine', 'ai_generated']
    search_fields = ['title', 'description', 'tags__name']
    ordering_fields = ['created_at', 'prep_time', 'cook_time', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Recipe.objects.filter(is_public=True).select_related('created_by').prefetch_related('tags', 'ratings')
        
        # Filter by tags
        tags = self.request.query_params.get('tags')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            queryset = queryset.filter(tags__name__in=tag_list).distinct()
        
        # Filter by max cooking time
        max_time = self.request.query_params.get('max_time')
        if max_time:
            try:
                max_time = int(max_time)
                queryset = queryset.filter(prep_time__lte=max_time, cook_time__lte=max_time)
            except ValueError:
                pass
        
        # Filter by favorites (for authenticated users)
        favorites_only = self.request.query_params.get('favorites')
        if favorites_only and self.request.user.is_authenticated:
            favorited_recipes = RecipeFavorite.objects.filter(user=self.request.user).values_list('recipe_id', flat=True)
            queryset = queryset.filter(id__in=favorited_recipes)
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateUpdateSerializer
        return RecipeListSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a recipe"""
    queryset = Recipe.objects.all().select_related('created_by').prefetch_related(
        'ingredients', 'instructions', 'tags', 'ratings__user'
    )
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RecipeCreateUpdateSerializer
        return RecipeDetailSerializer
    
    def get_object(self):
        obj = super().get_object()
        
        # Check permissions for private recipes
        if not obj.is_public and obj.created_by != self.request.user:
            if not self.request.user.is_authenticated:
                self.permission_denied(self.request, message="Authentication required for private recipes.")
            else:
                self.permission_denied(self.request, message="You don't have permission to access this recipe.")
        
        return obj
    
    def perform_update(self, serializer):
        # Only allow owner to update
        if serializer.instance.created_by != self.request.user:
            self.permission_denied(self.request, message="You can only edit your own recipes.")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Only allow owner to delete
        if instance.created_by != self.request.user:
            self.permission_denied(self.request, message="You can only delete your own recipes.")
        instance.delete()


class MyRecipesView(generics.ListAPIView):
    """List current user's recipes"""
    serializer_class = RecipeListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Recipe.objects.filter(created_by=self.request.user).prefetch_related('tags', 'ratings')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_recipe(request, recipe_id):
    """Rate a recipe"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if user has already rated this recipe
    rating, created = RecipeRating.objects.get_or_create(
        recipe=recipe,
        user=request.user,
        defaults={
            'rating': request.data.get('rating'),
            'review': request.data.get('review', '')
        }
    )
    
    if not created:
        # Update existing rating
        rating.rating = request.data.get('rating', rating.rating)
        rating.review = request.data.get('review', rating.review)
        rating.save()
    
    serializer = RecipeRatingSerializer(rating)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, recipe_id):
    """Add or remove recipe from favorites"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if request.method == 'POST':
        favorite, created = RecipeFavorite.objects.get_or_create(
            recipe=recipe,
            user=request.user
        )
        if created:
            return Response({'message': 'Recipe added to favorites'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Recipe already in favorites'}, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        try:
            favorite = RecipeFavorite.objects.get(recipe=recipe, user=request.user)
            favorite.delete()
            return Response({'message': 'Recipe removed from favorites'}, status=status.HTTP_200_OK)
        except RecipeFavorite.DoesNotExist:
            return Response({'message': 'Recipe not in favorites'}, status=status.HTTP_404_NOT_FOUND)


class FavoritesView(generics.ListAPIView):
    """List user's favorite recipes"""
    serializer_class = RecipeFavoriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return RecipeFavorite.objects.filter(user=self.request.user).select_related('recipe')


class RecipeTagsView(generics.ListAPIView):
    """List all recipe tags"""
    queryset = RecipeTag.objects.all().order_by('name')
    serializer_class = RecipeTagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['GET'])
def recipe_stats(request):
    """Get recipe statistics"""
    stats = {
        'total_recipes': Recipe.objects.filter(is_public=True).count(),
        'total_ratings': RecipeRating.objects.count(),
        'average_rating': RecipeRating.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,        'popular_cuisines': list(
            Recipe.objects.filter(is_public=True)
            .values('cuisine')
            .annotate(count=Count('cuisine'))
            .order_by('-count')[:5]
        ),
        'popular_tags': list(
            RecipeTag.objects.annotate(recipe_count=Count('recipes'))
            .order_by('-recipe_count')[:10]
            .values('name', 'recipe_count')
        )
    }
    return Response(stats)
