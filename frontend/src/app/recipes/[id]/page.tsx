'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Recipe } from '@/types/recipe';
import { recipeAPI } from '@/lib/api';
import { Clock, Users, ChefHat, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';

export default function RecipeDetailPage() {
  const params = useParams();
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (params.id) {
      loadRecipe(params.id as string);
    }
  }, [params.id]);

  const loadRecipe = async (id: string) => {
    try {
      const response = await recipeAPI.getRecipe(id);
      setRecipe(response.data);
    } catch (error) {
      console.error('Error loading recipe:', error);
      // Mock data for demo
      setRecipe({
        id: '1',
        name: 'Pasta Carbonara',
        description: 'Classic Italian pasta dish with eggs, cheese, and pancetta. A simple yet elegant meal that brings the authentic taste of Rome to your kitchen.',
        ingredients: [
          { name: 'Spaghetti', amount: '400', unit: 'g' },
          { name: 'Large eggs', amount: '4', unit: 'pieces' },
          { name: 'Pancetta', amount: '200', unit: 'g' },
          { name: 'Parmesan cheese', amount: '100', unit: 'g' },
          { name: 'Black pepper', amount: '1', unit: 'tsp' },
          { name: 'Salt', amount: 'to taste', unit: '' }
        ],
        instructions: [
          'Bring a large pot of salted water to boil and cook spaghetti according to package directions until al dente.',
          'While pasta cooks, cut pancetta into small cubes and cook in a large skillet over medium heat until crispy.',
          'In a bowl, whisk together eggs, grated Parmesan cheese, and freshly cracked black pepper.',
          'When pasta is ready, reserve 1 cup of pasta water and drain the rest.',
          'Add hot pasta to the skillet with pancetta and toss to combine.',
          'Remove from heat and quickly mix in the egg mixture, tossing constantly to prevent scrambling.',
          'Add pasta water gradually until you achieve a creamy consistency.',
          'Serve immediately with extra Parmesan and black pepper.'
        ],
        prep_time: 15,
        cook_time: 20,
        servings: 4,
        difficulty: 'medium',
        tags: ['italian', 'pasta', 'quick', 'dinner'],
        created_at: new Date().toISOString()
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600"></div>
      </div>
    );
  }

  if (!recipe) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Recipe not found</h2>
          <Link href="/recipes" className="text-orange-600 hover:text-orange-700">
            Back to recipes
          </Link>
        </div>
      </div>
    );
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <Link 
          href="/recipes"
          className="inline-flex items-center text-orange-600 hover:text-orange-700 mb-6"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to recipes
        </Link>

        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          {recipe.image_url && (
            <div className="relative h-64 w-full">
              <Image
                src={recipe.image_url}
                alt={recipe.name}
                fill
                className="object-cover"
              />
            </div>
          )}

          <div className="p-8">
            <div className="mb-6">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">{recipe.name}</h1>
              <p className="text-lg text-gray-600 mb-4">{recipe.description}</p>
              
              <div className="flex items-center space-x-6 mb-4">
                <div className="flex items-center text-gray-600">
                  <Clock className="w-5 h-5 mr-2" />
                  <span>Prep: {recipe.prep_time}m | Cook: {recipe.cook_time}m</span>
                </div>
                <div className="flex items-center text-gray-600">
                  <Users className="w-5 h-5 mr-2" />
                  <span>{recipe.servings} servings</span>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(recipe.difficulty)}`}>
                  {recipe.difficulty}
                </span>
              </div>

              {recipe.tags && recipe.tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {recipe.tags.map((tag, index) => (
                    <span 
                      key={index}
                      className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h2 className="text-xl font-semibold mb-4 flex items-center">
                  <ChefHat className="w-5 h-5 mr-2" />
                  Ingredients
                </h2>
                <ul className="space-y-2">
                  {recipe.ingredients.map((ingredient, index) => (
                    <li key={index} className="flex items-center">
                      <span className="w-2 h-2 bg-orange-600 rounded-full mr-3"></span>
                      <span>
                        {ingredient.amount} {ingredient.unit} {ingredient.name}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h2 className="text-xl font-semibold mb-4">Instructions</h2>
                <ol className="space-y-4">
                  {recipe.instructions.map((instruction, index) => (
                    <li key={index} className="flex">
                      <span className="flex-shrink-0 w-6 h-6 bg-orange-600 text-white rounded-full flex items-center justify-center text-sm font-medium mr-3 mt-0.5">
                        {index + 1}
                      </span>
                      <span className="text-gray-700">{instruction}</span>
                    </li>
                  ))}
                </ol>
              </div>
            </div>

            {recipe.nutrition && (
              <div className="mt-8 p-4 bg-gray-50 rounded-lg">
                <h3 className="text-lg font-semibold mb-3">Nutrition Information (per serving)</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="font-semibold text-lg">{recipe.nutrition.calories}</div>
                    <div className="text-sm text-gray-600">Calories</div>
                  </div>
                  <div className="text-center">
                    <div className="font-semibold text-lg">{recipe.nutrition.protein}g</div>
                    <div className="text-sm text-gray-600">Protein</div>
                  </div>
                  <div className="text-center">
                    <div className="font-semibold text-lg">{recipe.nutrition.carbs}g</div>
                    <div className="text-sm text-gray-600">Carbs</div>
                  </div>
                  <div className="text-center">
                    <div className="font-semibold text-lg">{recipe.nutrition.fat}g</div>
                    <div className="text-sm text-gray-600">Fat</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}