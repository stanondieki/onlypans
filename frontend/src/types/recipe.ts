export interface Recipe {
  id: string;
  title: string;
  description: string;
  image?: string;
  prep_time: number;
  cook_time: number;
  total_time?: number;
  servings: number;
  difficulty: 'easy' | 'medium' | 'hard';
  cuisine: string;
  created_by?: string;
  created_by_name?: string;
  created_at: string;
  updated_at?: string;
  is_public?: boolean;
  
  // Nutritional information
  calories_per_serving?: number;
  protein_grams?: number;
  carbs_grams?: number;
  fat_grams?: number;
  fiber_grams?: number;
  
  // AI generated fields
  ai_generated?: boolean;
  source_image?: string;
  
  // Related data
  ingredients: Ingredient[];
  instructions: Instruction[];
  tags: RecipeTag[];
  ratings?: RecipeRating[];
  average_rating?: number;
  is_favorited?: boolean;
  user_rating?: RecipeRating;
}

export interface Ingredient {
  id?: string;
  name: string;
  quantity: number;
  unit: string;
  notes?: string;
  order: number;
}

export interface Instruction {
  id?: string;
  step_number: number;
  instruction: string;
  time_minutes?: number;
  temperature?: string;
}

export interface RecipeTag {
  id: string;
  name: string;
}

export interface RecipeRating {
  id: string;
  rating: number;
  review?: string;
  user_name?: string;
  created_at: string;
}

export interface NutritionInfo {
  calories?: number;
  protein?: number;
  carbs?: number;
  fat?: number;
  fiber?: number;
}

export type RecipeDifficulty = 'easy' | 'medium' | 'hard';

export interface RecipeCreateData {
  title: string;
  description: string;
  image?: File;
  prep_time: number;
  cook_time: number;
  servings: number;
  difficulty: RecipeDifficulty;
  cuisine: string;
  is_public?: boolean;
  calories_per_serving?: number;
  protein_grams?: number;
  carbs_grams?: number;
  fat_grams?: number;
  fiber_grams?: number;
  ingredients: Omit<Ingredient, 'id'>[];
  instructions: Omit<Instruction, 'id'>[];
  tags?: string[];
}
