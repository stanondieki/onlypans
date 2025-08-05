export interface Meal {
  id: string;
  name: string;
  date: string;
  time: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  recipe_id?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface MealPlan {
  id: string;
  week_start: string;
  meals: Meal[];
  user_id: string;
}

export type MealTime = 'breakfast' | 'lunch' | 'dinner' | 'snack';
