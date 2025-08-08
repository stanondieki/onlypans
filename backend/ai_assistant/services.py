import os
import time
import json
import logging
from typing import Dict, List, Optional, Tuple
from django.conf import settings
from django.core.files.base import ContentFile
import google.generativeai as genai
from PIL import Image
from io import BytesIO

from recipes.models import Recipe, Ingredient, Instruction, RecipeTag
from .models import AIRequest, FoodRecognition, RecipeGeneration

logger = logging.getLogger(__name__)


class GeminiAIService:
    """Service class for interacting with Google Gemini AI"""
    
    def __init__(self):
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            logger.warning("Google API key not configured. AI features will not work.")
            self.model = None
    
    def is_available(self) -> bool:
        """Check if the AI service is available"""
        return self.model is not None and bool(settings.GOOGLE_API_KEY)
    
    def recognize_food_from_image(self, image_file, user) -> Tuple[AIRequest, Dict]:
        """
        Recognize food items from an uploaded image
        
        Args:
            image_file: Django uploaded file
            user: Django User instance
            
        Returns:
            Tuple of (AIRequest instance, response data)
        """
        start_time = time.time()
        
        # Create AI request record
        ai_request = AIRequest.objects.create(
            user=user,
            request_type='image_recognition',
            input_image=image_file
        )
        
        try:
            if not self.is_available():
                raise Exception("AI service is not available. Please check API configuration.")
            
            # Prepare the image
            image = Image.open(image_file)
            
            # Create prompt for food recognition
            prompt = """
            Analyze this image and identify any food items, dishes, or ingredients you can see.
            
            Please provide your response in the following JSON format:
            {
                "detected_foods": [
                    {
                        "name": "food item name",
                        "confidence": 0.95,
                        "category": "ingredient/dish/beverage",
                        "description": "brief description"
                    }
                ],
                "overall_confidence": 0.90,
                "suggestions": [
                    "Recipe suggestion 1",
                    "Recipe suggestion 2"
                ]
            }
            
            Focus on identifying:
            - Individual ingredients (vegetables, proteins, spices, etc.)
            - Prepared dishes or meals
            - Cooking implements or kitchen tools (if relevant)
            - Overall meal type (breakfast, lunch, dinner, snack)
            """
            
            # Generate response
            response = self.model.generate_content([prompt, image])
            response_text = response.text
            
            # Try to parse JSON response
            try:
                response_data = json.loads(response_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response
                response_data = {
                    "detected_foods": [],
                    "overall_confidence": 0.5,
                    "suggestions": [],
                    "raw_response": response_text
                }
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Update AI request
            ai_request.response_text = response_text
            ai_request.processing_time = processing_time
            ai_request.save()
            
            # Create FoodRecognition record
            FoodRecognition.objects.create(
                ai_request=ai_request,
                detected_foods=response_data.get('detected_foods', []),
                confidence_score=response_data.get('overall_confidence', 0.5)
            )
            
            return ai_request, response_data
            
        except Exception as e:
            logger.error(f"Error in food recognition: {str(e)}")
            ai_request.response_text = f"Error: {str(e)}"
            ai_request.processing_time = time.time() - start_time
            ai_request.save()
            
            return ai_request, {
                "error": str(e),
                "detected_foods": [],
                "overall_confidence": 0.0,
                "suggestions": []
            }
    
    def generate_recipe_from_ingredients(self, ingredients: str, user, **kwargs) -> Tuple[AIRequest, Dict]:
        """
        Generate a recipe based on available ingredients
        
        Args:
            ingredients: String of comma-separated ingredients
            user: Django User instance
            **kwargs: Additional parameters (dietary_restrictions, cuisine_preference, etc.)
            
        Returns:
            Tuple of (AIRequest instance, response data)
        """
        start_time = time.time()
        
        # Create AI request record
        ai_request = AIRequest.objects.create(
            user=user,
            request_type='recipe_generation',
            input_text=ingredients
        )
        
        try:
            if not self.is_available():
                raise Exception("AI service is not available. Please check API configuration.")
            
            # Extract parameters
            dietary_restrictions = kwargs.get('dietary_restrictions', '')
            cuisine_preference = kwargs.get('cuisine_preference', '')
            difficulty_preference = kwargs.get('difficulty_preference', 'medium')
            time_constraint = kwargs.get('time_constraint', None)
            servings = kwargs.get('servings', 4)
            
            # Create detailed prompt
            prompt = f"""
            Create a detailed recipe using primarily these ingredients: {ingredients}
            
            Requirements:
            - Servings: {servings}
            - Difficulty: {difficulty_preference}
            {f"- Dietary restrictions: {dietary_restrictions}" if dietary_restrictions else ""}
            {f"- Cuisine preference: {cuisine_preference}" if cuisine_preference else ""}
            {f"- Maximum cooking time: {time_constraint} minutes" if time_constraint else ""}
            
            Please provide your response in the following JSON format:
            {{
                "recipe": {{
                    "title": "Recipe Name",
                    "description": "Brief description of the dish",
                    "prep_time": 15,
                    "cook_time": 30,
                    "servings": {servings},
                    "difficulty": "{difficulty_preference}",
                    "cuisine": "cuisine type",
                    "ingredients": [
                        {{
                            "name": "ingredient name",
                            "quantity": 2,
                            "unit": "cups",
                            "notes": "optional notes"
                        }}
                    ],
                    "instructions": [
                        {{
                            "step_number": 1,
                            "instruction": "Detailed instruction for this step",
                            "time_minutes": 5,
                            "temperature": "350°F (optional)"
                        }}
                    ],
                    "tags": ["tag1", "tag2"],
                    "nutrition": {{
                        "calories_per_serving": 350,
                        "protein_grams": 25,
                        "carbs_grams": 30,
                        "fat_grams": 15,
                        "fiber_grams": 5
                    }}
                }},
                "confidence": 0.9,
                "notes": "Any additional cooking tips or variations"
            }}
            
            Make sure the recipe is practical, uses common cooking techniques, and includes all necessary steps.
            """
            
            # Generate response
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Try to parse JSON response
            try:
                response_data = json.loads(response_text)
                recipe_data = response_data.get('recipe', {})
                
                # Create Recipe object if parsing successful
                generated_recipe = self._create_recipe_from_ai_response(recipe_data, user)
                ai_request.generated_recipe = generated_recipe
                
            except (json.JSONDecodeError, Exception) as e:
                logger.error(f"Error parsing recipe JSON: {str(e)}")
                response_data = {
                    "error": "Failed to parse recipe",
                    "raw_response": response_text,
                    "confidence": 0.0
                }
                generated_recipe = None
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Update AI request
            ai_request.response_text = response_text
            ai_request.processing_time = processing_time
            ai_request.save()
            
            # Create RecipeGeneration record
            RecipeGeneration.objects.create(
                ai_request=ai_request,
                ingredients_provided=ingredients,
                dietary_restrictions=dietary_restrictions,
                cuisine_preference=cuisine_preference,
                difficulty_preference=difficulty_preference,
                time_constraint=time_constraint
            )
            
            return ai_request, response_data
            
        except Exception as e:
            logger.error(f"Error in recipe generation: {str(e)}")
            ai_request.response_text = f"Error: {str(e)}"
            ai_request.processing_time = time.time() - start_time
            ai_request.save()
            
            return ai_request, {
                "error": str(e),
                "confidence": 0.0
            }
    
    def _create_recipe_from_ai_response(self, recipe_data: Dict, user) -> Optional[Recipe]:
        """
        Create a Recipe object from AI response data
        
        Args:
            recipe_data: Dictionary containing recipe information
            user: Django User instance
            
        Returns:
            Recipe instance or None if creation fails
        """
        try:
            # Create Recipe
            recipe = Recipe.objects.create(
                title=recipe_data.get('title', 'AI Generated Recipe'),
                description=recipe_data.get('description', ''),
                prep_time=recipe_data.get('prep_time', 30),
                cook_time=recipe_data.get('cook_time', 30),
                servings=recipe_data.get('servings', 4),
                difficulty=recipe_data.get('difficulty', 'medium'),
                cuisine=recipe_data.get('cuisine', 'other'),
                created_by=user,
                ai_generated=True,
                # Nutrition data
                calories_per_serving=recipe_data.get('nutrition', {}).get('calories_per_serving'),
                protein_grams=recipe_data.get('nutrition', {}).get('protein_grams'),
                carbs_grams=recipe_data.get('nutrition', {}).get('carbs_grams'),
                fat_grams=recipe_data.get('nutrition', {}).get('fat_grams'),
                fiber_grams=recipe_data.get('nutrition', {}).get('fiber_grams')
            )
            
            # Create Ingredients
            for idx, ingredient_data in enumerate(recipe_data.get('ingredients', [])):
                Ingredient.objects.create(
                    recipe=recipe,
                    name=ingredient_data.get('name', ''),
                    quantity=ingredient_data.get('quantity', 1),
                    unit=ingredient_data.get('unit', 'piece'),
                    notes=ingredient_data.get('notes', ''),
                    order=idx + 1
                )
            
            # Create Instructions
            for instruction_data in recipe_data.get('instructions', []):
                Instruction.objects.create(
                    recipe=recipe,
                    step_number=instruction_data.get('step_number', 1),
                    instruction=instruction_data.get('instruction', ''),
                    time_minutes=instruction_data.get('time_minutes'),
                    temperature=instruction_data.get('temperature', '')
                )
            
            # Create Tags
            for tag_name in recipe_data.get('tags', []):
                tag, created = RecipeTag.objects.get_or_create(name=tag_name.lower())
                recipe.tags.add(tag)
            
            return recipe
            
        except Exception as e:
            logger.error(f"Error creating recipe from AI response: {str(e)}")
            return None
    
    def suggest_meal_planning(self, user_preferences: Dict, meal_history: List[Dict]) -> Dict:
        """
        Generate meal planning suggestions based on user preferences and history
        
        Args:
            user_preferences: Dictionary of user dietary preferences
            meal_history: List of recent meals
            
        Returns:
            Dictionary with meal suggestions
        """
        if not self.is_available():
            return {"error": "AI service not available"}
        
        try:
            prompt = f"""
            Based on the following user preferences and meal history, suggest a week's worth of meals:
            
            User Preferences: {json.dumps(user_preferences)}
            Recent Meal History: {json.dumps(meal_history)}
            
            Please provide suggestions for breakfast, lunch, and dinner for 7 days.
            Consider variety, nutrition balance, and user preferences.
            
            Format the response as JSON with meal suggestions for each day.
            """
            
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
            
        except Exception as e:
            logger.error(f"Error in meal planning: {str(e)}")
            return {"error": str(e)}
