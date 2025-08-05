import { create } from 'zustand';
import { Recipe } from '@/types/recipe';
import { Meal, MealPlan } from '@/types/meal';

interface AppState {
  // Recipes
  recipes: Recipe[];
  currentRecipe: Recipe | null;
  
  // Meals
  meals: Meal[];
  currentMealPlan: MealPlan | null;
  
  // UI state
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setRecipes: (recipes: Recipe[]) => void;
  setCurrentRecipe: (recipe: Recipe | null) => void;
  setMeals: (meals: Meal[]) => void;
  setCurrentMealPlan: (mealPlan: MealPlan | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useStore = create<AppState>((set) => ({
  // Initial state
  recipes: [],
  currentRecipe: null,
  meals: [],
  currentMealPlan: null,
  isLoading: false,
  error: null,
  
  // Actions
  setRecipes: (recipes) => set({ recipes }),
  setCurrentRecipe: (recipe) => set({ currentRecipe: recipe }),
  setMeals: (meals) => set({ meals }),
  setCurrentMealPlan: (mealPlan) => set({ currentMealPlan: mealPlan }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
}));
