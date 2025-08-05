from django.contrib import admin
from .models import Recipe, Ingredient, Instruction, RecipeTag, RecipeRating, RecipeFavorite


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1
    fields = ['name', 'quantity', 'unit', 'notes', 'order']
    ordering = ['order']


class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 1
    fields = ['step_number', 'instruction', 'time_minutes', 'temperature']
    ordering = ['step_number']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'cuisine', 'difficulty', 'prep_time', 'cook_time', 'servings', 'created_by', 'is_public', 'ai_generated', 'created_at']
    list_filter = ['cuisine', 'difficulty', 'is_public', 'ai_generated', 'created_at']
    search_fields = ['title', 'description', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at', 'average_rating', 'total_time']
    # filter_horizontal = ['tags']  # This doesn't work for reverse M2M relationships
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Recipe Details', {
            'fields': ('prep_time', 'cook_time', 'total_time', 'servings', 'difficulty', 'cuisine')
        }),
        ('Nutritional Information', {
            'fields': ('calories_per_serving', 'protein_grams', 'carbs_grams', 'fat_grams', 'fiber_grams'),
            'classes': ('collapse',)
        }),
        ('Meta Information', {
            'fields': ('created_by', 'is_public', 'ai_generated', 'source_image', 'tags')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [IngredientInline, InstructionInline]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['created_by']
        return self.readonly_fields


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'recipe_count']
    search_fields = ['name']
    
    def recipe_count(self, obj):
        return obj.recipes.count()
    recipe_count.short_description = 'Recipe Count'


@admin.register(RecipeRating)
class RecipeRatingAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['recipe__title', 'user__username']
    readonly_fields = ['created_at']


@admin.register(RecipeFavorite)
class RecipeFavoriteAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['recipe__title', 'user__username']
    readonly_fields = ['created_at']
