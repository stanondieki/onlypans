from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import models

from .models import AIRequest, AIFeedback
from .serializers import (
    AIRequestSerializer, AIRequestCreateSerializer, AIFeedbackSerializer,
    ImageRecognitionRequestSerializer, RecipeGenerationRequestSerializer,
    AIResponseSerializer
)
from .services import GeminiAIService


class AIRequestListView(generics.ListAPIView):
    """List user's AI requests"""
    serializer_class = AIRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AIRequest.objects.filter(user=self.request.user).order_by('-created_at')


class AIRequestDetailView(generics.RetrieveAPIView):
    """Get details of a specific AI request"""
    serializer_class = AIRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AIRequest.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_chat(request):
    """General AI chat endpoint for any cooking/food related questions"""
    question = request.data.get('question', '')
    context = request.data.get('context', '')  # Optional context for follow-up questions
    
    if not question.strip():
        return Response({
            'success': False,
            'message': 'Question is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    ai_service = GeminiAIService()
    
    if not ai_service.is_available():
        return Response({
            'success': False,
            'message': 'AI service is currently unavailable. Please check your API configuration.'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        import time
        start_time = time.time()
        
        # Create AI request
        ai_request = AIRequest.objects.create(
            user=request.user,
            request_type='general_chat',
            input_text=f"Question: {question}\nContext: {context}" if context else question
        )
        
        # Enhanced prompt for food/cooking related questions
        prompt = f"""
        You are OnlyPans AI, a knowledgeable cooking and food assistant. Answer the following question with helpful, accurate, and practical information.
        
        Question: {question}
        {f"Previous context: {context}" if context else ""}
        
        Guidelines:
        - Focus on cooking, recipes, nutrition, meal planning, and food-related topics
        - Provide practical, actionable advice
        - If the question is not food-related, politely redirect to cooking topics
        - Be conversational but informative
        - Include tips, substitutions, or variations when relevant
        - If suggesting recipes, provide brief ingredients and steps
        
        Please provide a helpful and engaging response:
        """
        
        response = ai_service.model.generate_content(prompt)
        response_text = response.text
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Update AI request
        ai_request.response_text = response_text
        ai_request.processing_time = processing_time
        ai_request.save()
        
        return Response({
            'success': True,
            'message': 'AI response generated successfully',
            'data': {
                'response': response_text,
                'question': question,
                'context': context
            },
            'processing_time': processing_time,
            'request_id': ai_request.id
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error generating AI response: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recognize_food_image(request):
    """Recognize food items from an uploaded image"""
    serializer = ImageRecognitionRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        image_file = serializer.validated_data['image']
        
        # Use AI service to recognize food
        ai_service = GeminiAIService()
        
        if not ai_service.is_available():
            return Response({
                'success': False,
                'message': 'AI service is currently unavailable. Please check your API configuration.'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        try:
            ai_request, response_data = ai_service.recognize_food_from_image(image_file, request.user)
            
            response_serializer = AIResponseSerializer(data={
                'success': True,
                'message': 'Food recognition completed successfully',
                'data': response_data,
                'processing_time': ai_request.processing_time,
                'request_id': ai_request.id
            })
            
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error processing image: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_recipe(request):
    """Generate a recipe from ingredients"""
    serializer = RecipeGenerationRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        ingredients = serializer.validated_data['ingredients']
        
        # Extract optional parameters
        kwargs = {
            'dietary_restrictions': serializer.validated_data.get('dietary_restrictions', ''),
            'cuisine_preference': serializer.validated_data.get('cuisine_preference', ''),
            'difficulty_preference': serializer.validated_data.get('difficulty_preference', 'medium'),
            'time_constraint': serializer.validated_data.get('time_constraint'),
            'servings': serializer.validated_data.get('servings', 4)
        }
        
        # Use AI service to generate recipe
        ai_service = GeminiAIService()
        
        if not ai_service.is_available():
            return Response({
                'success': False,
                'message': 'AI service is currently unavailable. Please check your API configuration.'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        try:
            ai_request, response_data = ai_service.generate_recipe_from_ingredients(
                ingredients, request.user, **kwargs
            )
            
            response_serializer = AIResponseSerializer(data={
                'success': True,
                'message': 'Recipe generation completed successfully',
                'data': response_data,
                'processing_time': ai_request.processing_time,
                'request_id': ai_request.id
            })
            
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error generating recipe: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def suggest_ingredients(request):
    """Suggest ingredients based on user input"""
    input_text = request.data.get('input_text', '')
    
    if not input_text.strip():
        return Response({
            'success': False,
            'message': 'Input text is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    ai_service = GeminiAIService()
    
    if not ai_service.is_available():
        return Response({
            'success': False,
            'message': 'AI service is currently unavailable.'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        # Create AI request
        ai_request = AIRequest.objects.create(
            user=request.user,
            request_type='ingredient_suggestion',
            input_text=input_text
        )
        
        # Generate ingredient suggestions using Gemini
        prompt = f"""
        Based on the following input: "{input_text}"
        
        Suggest complementary ingredients that would work well together for cooking.
        Consider flavor profiles, nutritional balance, and common cooking combinations.
        
        Provide your response as a JSON array of ingredient suggestions:
        {{
            "suggestions": [
                {{
                    "ingredient": "ingredient name",
                    "reason": "why this ingredient works well",
                    "category": "protein/vegetable/grain/spice/etc"
                }}
            ]
        }}
        """
        
        response = ai_service.model.generate_content(prompt)
        
        # Update AI request
        ai_request.response_text = response.text
        ai_request.save()
        
        return Response({
            'success': True,
            'message': 'Ingredient suggestions generated successfully',
            'data': {'suggestions': response.text},
            'request_id': ai_request.id
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error generating suggestions: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_feedback(request, request_id):
    """Submit feedback for an AI request"""
    ai_request = get_object_or_404(AIRequest, id=request_id, user=request.user)
    
    serializer = AIFeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            ai_request=ai_request,
            user=request.user
        )
        return Response({
            'message': 'Feedback submitted successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([])  # Allow anonymous access
def ai_service_status(request):
    """Check AI service availability"""
    ai_service = GeminiAIService()
    
    return Response({
        'available': ai_service.is_available(),
        'message': 'AI service is available' if ai_service.is_available() else 'AI service is not configured or unavailable'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_ai_stats(request):
    """Get user's AI usage statistics"""
    user_requests = AIRequest.objects.filter(user=request.user)
    
    stats = {
        'total_requests': user_requests.count(),
        'by_type': {
            'image_recognition': user_requests.filter(request_type='image_recognition').count(),
            'recipe_generation': user_requests.filter(request_type='recipe_generation').count(),
            'ingredient_suggestion': user_requests.filter(request_type='ingredient_suggestion').count(),
            'meal_planning': user_requests.filter(request_type='meal_planning').count(),
        },
        'recipes_generated': user_requests.filter(
            request_type='recipe_generation',
            generated_recipe__isnull=False
        ).count(),
        'avg_processing_time': user_requests.exclude(
            processing_time__isnull=True
        ).aggregate(avg_time=models.Avg('processing_time'))['avg_time'] or 0,
    }
    
    return Response(stats)
