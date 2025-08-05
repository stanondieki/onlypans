from django.contrib import admin
from .models import AIRequest, FoodRecognition, RecipeGeneration, AIFeedback


class FoodRecognitionInline(admin.StackedInline):
    model = FoodRecognition
    can_delete = False
    readonly_fields = ['detected_foods', 'confidence_score']


class RecipeGenerationInline(admin.StackedInline):
    model = RecipeGeneration
    can_delete = False
    readonly_fields = ['ingredients_provided', 'dietary_restrictions', 'cuisine_preference', 'difficulty_preference', 'time_constraint']


@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'request_type', 'processing_time', 'has_generated_recipe', 'created_at']
    list_filter = ['request_type', 'created_at']
    search_fields = ['user__username', 'input_text']
    readonly_fields = ['created_at', 'processing_time']
    
    fieldsets = (
        ('Request Info', {
            'fields': ('user', 'request_type', 'input_text', 'input_image')
        }),
        ('Response', {
            'fields': ('response_text', 'generated_recipe', 'processing_time')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_generated_recipe(self, obj):
        return obj.generated_recipe is not None
    has_generated_recipe.boolean = True
    has_generated_recipe.short_description = 'Recipe Generated'
    
    def get_inlines(self, request, obj):
        inlines = []
        if obj and obj.request_type == 'image_recognition':
            inlines.append(FoodRecognitionInline)
        elif obj and obj.request_type == 'recipe_generation':
            inlines.append(RecipeGenerationInline)
        return inlines


@admin.register(AIFeedback)
class AIFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'ai_request', 'feedback_type', 'created_at']
    list_filter = ['feedback_type', 'created_at']
    search_fields = ['user__username', 'comment']
    readonly_fields = ['created_at']
