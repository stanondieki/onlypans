'use client';

import { useState, useEffect } from 'react';
import { format, startOfWeek, addDays, isSameDay } from 'date-fns';
import { Meal, MealTime } from '@/types/meal';
import { mealAPI } from '@/lib/api';
import { Plus, Edit, Trash2, ChevronLeft, ChevronRight, Calendar } from 'lucide-react';

interface MealScheduleProps {
  onAddMeal?: (date: string, time: MealTime) => void;
  onEditMeal?: (meal: Meal) => void;
}

export default function MealSchedule({ onAddMeal, onEditMeal }: MealScheduleProps) {
  const [currentWeek, setCurrentWeek] = useState(new Date());
  const [meals, setMeals] = useState<Meal[]>([]);
  const [loading, setLoading] = useState(false);

  const weekStart = startOfWeek(currentWeek, { weekStartsOn: 1 }); // Monday start
  const weekDays = Array.from({ length: 7 }, (_, i) => addDays(weekStart, i));
  const mealTimes: MealTime[] = ['breakfast', 'lunch', 'dinner', 'snack'];

  const mealTimeColors = {
    breakfast: 'from-yellow-400 to-orange-400',
    lunch: 'from-green-400 to-teal-400',
    dinner: 'from-blue-400 to-purple-400',
    snack: 'from-pink-400 to-rose-400'
  };
  const mealTimeIcons = {
    breakfast: '🌅',
    lunch: '☀️',
    dinner: '🌙',
    snack: '🍓'
  };

  useEffect(() => {
    const loadMealsData = async () => {
      setLoading(true);
      try {
        const response = await mealAPI.getMealPlan(format(weekStart, 'yyyy-MM-dd'));
        setMeals(response.data.meals || []);
      } catch (error) {
        console.error('Error loading meals:', error);
      } finally {
        setLoading(false);
      }
    };

    loadMealsData();
  }, [weekStart]);

  const getMealsForSlot = (date: Date, time: MealTime) => {
    return meals.filter(meal => 
      isSameDay(new Date(meal.date), date) && meal.time === time
    );
  };

  const handleDeleteMeal = async (mealId: string) => {
    try {
      await mealAPI.deleteMeal(mealId);
      setMeals(meals.filter(meal => meal.id !== mealId));
    } catch (error) {
      console.error('Error deleting meal:', error);
    }
  };

  return (
    <div className="space-y-6">
      {/* Week Navigation */}
      <div className="flex items-center justify-between bg-gradient-to-r from-orange-50 to-red-50 rounded-2xl p-6">
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl flex items-center justify-center">
            <Calendar className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Week of {format(weekStart, 'MMM d, yyyy')}
            </h2>
            <p className="text-gray-600">Plan your perfect week</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setCurrentWeek(addDays(currentWeek, -7))}
            className="flex items-center space-x-2 px-4 py-2 bg-white/80 backdrop-blur-sm border border-orange-200 rounded-xl hover:bg-white hover:shadow-lg transition-all duration-300"
          >
            <ChevronLeft className="w-4 h-4" />
            <span className="font-medium">Previous</span>
          </button>
          <button
            onClick={() => setCurrentWeek(new Date())}
            className="px-4 py-2 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-xl hover:from-orange-600 hover:to-red-600 transition-all duration-300 font-medium"
          >
            This Week
          </button>
          <button
            onClick={() => setCurrentWeek(addDays(currentWeek, 7))}
            className="flex items-center space-x-2 px-4 py-2 bg-white/80 backdrop-blur-sm border border-orange-200 rounded-xl hover:bg-white hover:shadow-lg transition-all duration-300"
          >
            <span className="font-medium">Next</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Schedule Grid */}
      <div className="grid grid-cols-8 gap-4">
        {/* Header */}
        <div className=""></div>
        {weekDays.map((day, index) => (
          <div key={index} className="text-center p-4 bg-white rounded-2xl shadow-sm border border-gray-100">
            <div className="font-bold text-lg text-gray-900">{format(day, 'EEE')}</div>
            <div className="text-sm text-gray-500 mt-1">{format(day, 'MMM d')}</div>
            <div className={`mt-2 w-full h-1 rounded-full ${
              isSameDay(day, new Date()) ? 'bg-gradient-to-r from-orange-500 to-red-500' : 'bg-gray-200'
            }`}></div>
          </div>
        ))}

        {/* Meal rows */}
        {mealTimes.map((time) => (
          <div key={time} className="contents">
            <div className="flex items-center p-4 bg-white rounded-2xl shadow-sm border border-gray-100">
              <div className={`w-10 h-10 bg-gradient-to-r ${mealTimeColors[time]} rounded-xl flex items-center justify-center mr-3`}>
                <span className="text-xl">{mealTimeIcons[time]}</span>
              </div>
              <div>
                <div className="font-semibold text-gray-900 capitalize">{time}</div>
                <div className="text-xs text-gray-500">
                  {time === 'breakfast' && '7:00 - 9:00 AM'}
                  {time === 'lunch' && '12:00 - 2:00 PM'}
                  {time === 'dinner' && '6:00 - 8:00 PM'}
                  {time === 'snack' && 'Anytime'}
                </div>
              </div>
            </div>
            
            {weekDays.map((day, dayIndex) => {
              const slotMeals = getMealsForSlot(day, time);
              const dateStr = format(day, 'yyyy-MM-dd');
              
              return (
                <div 
                  key={`${time}-${dayIndex}`}
                  className="min-h-[140px] p-3 bg-gradient-to-br from-gray-50 to-white rounded-2xl border-2 border-dashed border-gray-200 hover:border-orange-300 transition-all duration-300 group"
                >
                  <div className="space-y-2 h-full flex flex-col">
                    {slotMeals.map((meal) => (
                      <div
                        key={meal.id}
                        className="bg-white rounded-xl p-3 shadow-sm border border-gray-100 group/meal hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="font-semibold text-sm text-gray-900 mb-1">{meal.name}</h4>
                            {meal.notes && (
                              <p className="text-xs text-gray-500 leading-relaxed">{meal.notes}</p>
                            )}
                          </div>
                          <div className="flex space-x-1 opacity-0 group-hover/meal:opacity-100 transition-opacity duration-200">
                            <button
                              onClick={() => onEditMeal?.(meal)}
                              className="p-1.5 text-blue-500 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-all duration-200"
                            >
                              <Edit className="w-3 h-3" />
                            </button>
                            <button
                              onClick={() => handleDeleteMeal(meal.id)}
                              className="p-1.5 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-lg transition-all duration-200"
                            >
                              <Trash2 className="w-3 h-3" />
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                    
                    <button
                      onClick={() => onAddMeal?.(dateStr, time)}
                      className="flex-1 min-h-[40px] border-2 border-dashed border-gray-300 rounded-xl flex items-center justify-center text-gray-400 hover:border-orange-400 hover:text-orange-600 hover:bg-orange-50 transition-all duration-300 group-hover:border-orange-300"
                    >
                      <div className="flex items-center space-x-2">
                        <Plus className="w-4 h-4" />
                        <span className="text-sm font-medium">Add Meal</span>
                      </div>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        ))}
      </div>

      {loading && (
        <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-8 shadow-2xl">
            <div className="flex items-center space-x-4">
              <div className="animate-spin rounded-full h-8 w-8 border-2 border-orange-200 border-t-orange-600"></div>
              <span className="font-medium text-gray-900">Loading meal plan...</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
