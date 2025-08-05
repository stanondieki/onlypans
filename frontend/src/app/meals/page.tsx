'use client';

import { useState } from 'react';
import MealSchedule from '@/components/MealSchedule';
import { Meal, MealTime } from '@/types/meal';
import { Calendar, ChefHat, Clock, Plus, Star, TrendingUp } from 'lucide-react';

export default function MealsPage() {
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState<{ date: string; time: MealTime } | null>(null);

  const handleAddMeal = (date: string, time: MealTime) => {
    setSelectedSlot({ date, time });
    setShowAddModal(true);
  };

  const handleEditMeal = (meal: Meal) => {
    // TODO: Implement edit meal functionality
    console.log('Edit meal:', meal);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-red-50">
      {/* Header Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-orange-600 via-red-500 to-pink-500 text-white">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="relative">
                <Calendar className="w-16 h-16 text-white/90" />
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-yellow-400 rounded-full flex items-center justify-center">
                  <Star className="w-3 h-3 text-yellow-800" />
                </div>
              </div>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-white to-orange-100 bg-clip-text text-transparent">
              Weekly Meal Plan
            </h1>
            <p className="text-xl text-orange-100 max-w-3xl mx-auto leading-relaxed">
              Plan your meals for the week ahead. Click on any time slot to add a meal and create a 
              perfectly balanced dining schedule.
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-2xl shadow-lg p-6 border border-orange-100 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-r from-green-400 to-green-600 rounded-xl flex items-center justify-center">
                <ChefHat className="w-6 h-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">12</p>
                <p className="text-gray-600">Planned Meals</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6 border border-orange-100 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-400 to-blue-600 rounded-xl flex items-center justify-center">
                <Clock className="w-6 h-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">2.5h</p>
                <p className="text-gray-600">Avg Cook Time</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6 border border-orange-100 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-400 to-purple-600 rounded-xl flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">85%</p>
                <p className="text-gray-600">Plan Complete</p>
              </div>
            </div>
          </div>
        </div>

        {/* Meal Schedule */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-2xl border border-orange-200 overflow-hidden">
          <div className="bg-gradient-to-r from-orange-500 to-red-500 px-8 py-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-white">Your Weekly Schedule</h2>
              <button className="bg-white/20 backdrop-blur-sm text-white px-6 py-2 rounded-xl hover:bg-white/30 transition-all duration-300 flex items-center space-x-2">
                <Plus className="w-4 h-4" />
                <span>Quick Add</span>
              </button>
            </div>
          </div>
          
          <div className="p-8">
            <MealSchedule 
              onAddMeal={handleAddMeal}
              onEditMeal={handleEditMeal}
            />
          </div>
        </div>

        {/* Add Meal Modal - Enhanced */}
        {showAddModal && selectedSlot && (
          <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-3xl shadow-2xl w-full max-w-md transform transition-all duration-300 scale-100">
              <div className="bg-gradient-to-r from-orange-500 to-red-500 px-6 py-4 rounded-t-3xl">
                <h3 className="text-xl font-bold text-white">
                  Add {selectedSlot.time} for {selectedSlot.date}
                </h3>
              </div>
              
              <div className="p-6">
                <div className="text-center py-8">
                  <div className="w-16 h-16 bg-gradient-to-r from-orange-100 to-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <ChefHat className="w-8 h-8 text-orange-600" />
                  </div>
                  <p className="text-gray-600 mb-6">
                    Enhanced meal planning functionality will be implemented in the next phase.
                  </p>
                  
                  <div className="flex space-x-3">
                    <button
                      onClick={() => setShowAddModal(false)}
                      className="flex-1 bg-gray-100 text-gray-700 px-4 py-3 rounded-xl hover:bg-gray-200 transition-colors duration-200 font-medium"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={() => setShowAddModal(false)}
                      className="flex-1 bg-gradient-to-r from-orange-500 to-red-500 text-white px-4 py-3 rounded-xl hover:from-orange-600 hover:to-red-600 transition-all duration-200 font-medium"
                    >
                      Got it
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}