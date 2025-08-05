from django.contrib import admin
from .models import MealPlan, Meal, ShoppingList, ShoppingListItem, MealRating


class MealInline(admin.TabularInline):
    model = Meal
    extra = 0
    fields = ['recipe', 'date', 'meal_type', 'servings', 'completed']
    readonly_fields = ['completed_at']


class ShoppingListItemInline(admin.TabularInline):
    model = ShoppingListItem
    extra = 0
    fields = ['ingredient_name', 'quantity', 'unit', 'category', 'purchased']


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'start_date', 'end_date', 'is_active', 'meal_count', 'created_at']
    list_filter = ['is_active', 'created_at', 'start_date']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'
    
    inlines = [MealInline]
    
    def meal_count(self, obj):
        return obj.meals.count()
    meal_count.short_description = 'Meals Count'


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'meal_plan', 'date', 'meal_type', 'servings', 'completed', 'created_at']
    list_filter = ['meal_type', 'completed', 'date', 'created_at']
    search_fields = ['recipe__title', 'meal_plan__name', 'meal_plan__user__username']
    readonly_fields = ['created_at', 'completed_at']
    date_hierarchy = 'date'


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['meal_plan', 'item_count', 'purchased_count', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    inlines = [ShoppingListItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Total Items'
    
    def purchased_count(self, obj):
        return obj.items.filter(purchased=True).count()
    purchased_count.short_description = 'Purchased Items'


@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ['ingredient_name', 'quantity', 'unit', 'category', 'purchased', 'shopping_list']
    list_filter = ['category', 'purchased', 'unit']
    search_fields = ['ingredient_name', 'shopping_list__meal_plan__name']


@admin.register(MealRating)
class MealRatingAdmin(admin.ModelAdmin):
    list_display = ['meal', 'user', 'rating', 'would_make_again', 'created_at']
    list_filter = ['rating', 'would_make_again', 'created_at']
    search_fields = ['meal__recipe__title', 'user__username']
    readonly_fields = ['created_at']
