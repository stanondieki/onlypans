'use client';

import { Recipe } from '@/types/recipe';
import { Clock, Users, ChefHat, Tag, Heart, Star, Bookmark, Utensils, Award } from 'lucide-react';
import Image from 'next/image';
import { useState } from 'react';

interface RecipeCardProps {
  recipe: Recipe;
  onClick?: () => void;
}

export default function RecipeCard({ recipe, onClick }: RecipeCardProps) {
  const [isFavorited, setIsFavorited] = useState(false);
  const [isBookmarked, setIsBookmarked] = useState(false);

  const getDifficultyBgColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100';
      case 'medium': return 'bg-orange-100';
      case 'hard': return 'bg-red-100';
      default: return 'bg-gray-100';
    }
  };

  const getDifficultyTextColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'text-green-800';
      case 'medium': return 'text-orange-800';
      case 'hard': return 'text-red-800';
      default: return 'text-gray-800';
    }
  };

  const handleFavorite = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsFavorited(!isFavorited);
  };

  const handleBookmark = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsBookmarked(!isBookmarked);
  };

  const totalTime = recipe.prep_time + recipe.cook_time;

  return (
    <div 
      onClick={onClick}
      className="group cursor-pointer bg-white/90 backdrop-blur-sm rounded-3xl shadow-lg border border-gray-200 overflow-hidden transition-all duration-500 hover:shadow-2xl hover:-translate-y-3 hover:border-orange-300"
    >
      {/* Image Section */}
      <div className="relative h-56 bg-gradient-to-br from-orange-100 via-red-100 to-pink-100 overflow-hidden">
        {recipe.image_url ? (
          <Image
            src={recipe.image_url}
            alt={recipe.name}
            fill
            className="object-cover transition-transform duration-500 group-hover:scale-110"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-orange-200 via-red-200 to-pink-200">
            <ChefHat className="w-16 h-16 text-orange-600/60" />
          </div>
        )}
        
        {/* Overlay Gradient */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        
        {/* Action Buttons */}
        <div className="absolute top-4 right-4 flex space-x-2">
          <button
            onClick={handleFavorite}
            className={`w-10 h-10 rounded-full backdrop-blur-sm border transition-all duration-300 flex items-center justify-center ${
              isFavorited 
                ? 'bg-red-500 border-red-500 text-white' 
                : 'bg-white/80 border-white/50 text-gray-600 hover:bg-red-50 hover:text-red-500'
            }`}
          >
            <Heart className={`w-5 h-5 ${isFavorited ? 'fill-current' : ''}`} />
          </button>
          <button
            onClick={handleBookmark}
            className={`w-10 h-10 rounded-full backdrop-blur-sm border transition-all duration-300 flex items-center justify-center ${
              isBookmarked 
                ? 'bg-blue-500 border-blue-500 text-white' 
                : 'bg-white/80 border-white/50 text-gray-600 hover:bg-blue-50 hover:text-blue-500'
            }`}
          >
            <Bookmark className={`w-5 h-5 ${isBookmarked ? 'fill-current' : ''}`} />
          </button>
        </div>

        {/* Difficulty Badge */}
        <div className="absolute top-4 left-4">
          <div className={`px-3 py-1 rounded-full backdrop-blur-sm border border-white/30 ${getDifficultyBgColor(recipe.difficulty)} ${getDifficultyTextColor(recipe.difficulty)}`}>
            <div className="flex items-center space-x-1">
              <Award className="w-3 h-3" />
              <span className="capitalize text-sm font-medium">{recipe.difficulty}</span>
            </div>
          </div>
        </div>

        {/* Recipe Rating */}
        <div className="absolute bottom-4 left-4">
          <div className="flex items-center space-x-1 bg-black/30 backdrop-blur-sm rounded-full px-3 py-1">
            <Star className="w-4 h-4 text-yellow-400 fill-current" />
            <span className="text-white text-sm font-medium">4.8</span>
          </div>
        </div>
      </div>

      {/* Content Section */}
      <div className="p-6">
        {/* Recipe Title */}
        <h3 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2 group-hover:text-orange-600 transition-colors duration-300">
          {recipe.name}
        </h3>

        {/* Recipe Description */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-2 leading-relaxed">
          {recipe.description}
        </p>

        {/* Recipe Stats */}
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-100 to-blue-200 rounded-lg flex items-center justify-center">
              <Clock className="w-4 h-4 text-blue-600" />
            </div>
            <div>
              <p className="text-xs text-gray-500">Total</p>
              <p className="text-sm font-semibold text-gray-900">{totalTime}m</p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-green-100 to-green-200 rounded-lg flex items-center justify-center">
              <Users className="w-4 h-4 text-green-600" />
            </div>
            <div>
              <p className="text-xs text-gray-500">Serves</p>
              <p className="text-sm font-semibold text-gray-900">{recipe.servings}</p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-100 to-purple-200 rounded-lg flex items-center justify-center">
              <Utensils className="w-4 h-4 text-purple-600" />
            </div>
            <div>
              <p className="text-xs text-gray-500">Steps</p>
              <p className="text-sm font-semibold text-gray-900">{recipe.instructions?.length || 0}</p>
            </div>
          </div>
        </div>

        {/* Tags */}
        {recipe.tags && recipe.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {recipe.tags.slice(0, 3).map((tag, index) => (
              <span
                key={index}
                className="inline-flex items-center space-x-1 px-3 py-1 bg-gradient-to-r from-orange-100 to-red-100 text-orange-700 text-xs font-medium rounded-full border border-orange-200"
              >
                <Tag className="w-3 h-3" />
                <span>{tag}</span>
              </span>
            ))}
            {recipe.tags.length > 3 && (
              <span className="inline-flex items-center px-3 py-1 bg-gray-100 text-gray-600 text-xs font-medium rounded-full">
                +{recipe.tags.length - 3} more
              </span>
            )}
          </div>
        )}

        {/* Action Button */}
        <button className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white py-3 px-4 rounded-xl font-semibold transition-all duration-300 hover:from-orange-600 hover:to-red-600 hover:shadow-lg transform hover:-translate-y-0.5 flex items-center justify-center space-x-2">
          <ChefHat className="w-5 h-5" />
          <span>View Recipe</span>
        </button>
      </div>
    </div>
  );
}
