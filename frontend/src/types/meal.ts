export interface Meal {
  id: string;
  recipe: string; // Recipe ID
  recipe_details?: {
    id: string;
    title: string;
    description?: string;
    image?: string;
    prep_time?: number;
    cook_time?: number;
    servings?: number;
    difficulty?: string;
    calories_per_serving?: number;
  };
  date: string;
  meal_type: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  servings: number;
  notes?: string;
  completed: boolean;
  completed_at?: string;
  created_at: string;
}

export interface MealPlan {
  id: string;
  name: string;
  start_date: string;
  end_date: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  meals?: Meal[];
  meals_by_date?: Record<string, Record<string, Meal | null>>;
  meals_count?: number;
}

export type MealTime = 'breakfast' | 'lunch' | 'dinner' | 'snack';
