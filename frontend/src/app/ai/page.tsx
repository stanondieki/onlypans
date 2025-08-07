'use client';

import { useState, useRef } from 'react';
import { Bot, Camera, ChefHat, MessageCircle, Send, Sparkles, Upload, X, AlertCircle, Wifi, WifiOff } from 'lucide-react';
import { aiAPI } from '@/lib/api';
import { enhancedAIAPI } from '@/lib/enhancedAIAPI';
import { mockAIAPI } from '@/lib/mockAPI';
import ConnectionDiagnostic from '@/components/ConnectionDiagnostic';

interface ChatMessage {
  id: string;
  type: 'user' | 'ai' | 'error';
  content: string;
  timestamp: Date;
}

interface AIResponse {
  success: boolean;
  message: string;
  data?: any;
  processing_time?: number;
  request_id?: string;
}

export default function AIAssistant() {
  const [activeTab, setActiveTab] = useState<'chat' | 'image' | 'recipe'>('chat');
  const [useMockAPI, setUseMockAPI] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'checking'>('checking');
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      type: 'ai',
      content: 'Hello! I\'m your OnlyPans AI assistant powered by Gemini AI. I can help you with cooking questions, analyze food images for recipes, or generate custom recipes from ingredients. What would you like to explore today?',
      timestamp: new Date()
    }
  ]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [ingredients, setIngredients] = useState('');
  const [preferences, setPreferences] = useState({
    dietary_restrictions: '',
    cuisine_preference: '',
    difficulty_preference: 'medium',
    servings: 4,
    time_constraint: ''
  });

  const fileInputRef = useRef<HTMLInputElement>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const addMessage = (type: 'user' | 'ai' | 'error', content: string) => {
    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      type,
      content,
      timestamp: new Date()
    };
    setChatMessages(prev => [...prev, newMessage]);
    setTimeout(scrollToBottom, 100);
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim() || loading) return;

    const userMessage = currentMessage;
    setCurrentMessage('');
    addMessage('user', userMessage);
    setLoading(true);

    try {
      let response;
      
      if (useMockAPI) {
        // Use mock API for immediate testing
        console.log('� Using mock API for message:', userMessage);
        const mockResponse = await mockAIAPI.chat(userMessage);
        addMessage('ai', mockResponse.response);
        console.log('✅ Mock response received');
      } else {
        // Try real API first
        console.log('�🚀 Sending chat message to real API:', userMessage);
        try {
          response = await enhancedAIAPI.chat(userMessage);
          
          if (response?.data?.success) {
            addMessage('ai', response.data.data.response);
            console.log('✅ Real API response received');
            setConnectionStatus('connected');
          } else {
            throw new Error(`API Error: ${response?.data?.message || 'Unknown error'}`);
          }
        } catch (realAPIError) {
          console.warn('⚠️ Real API failed, switching to mock mode:', realAPIError);
          setConnectionStatus('disconnected');
          setUseMockAPI(true);
          
          // Fall back to mock API
          const mockResponse = await mockAIAPI.chat(userMessage);
          addMessage('ai', `[Mock Mode] ${mockResponse.response}`);
        }
      }
    } catch (error: any) {
      console.error('❌ Chat error:', error);
      addMessage('error', 'Sorry, I\'m having trouble right now. Please check the connection diagnostic below.');
      setConnectionStatus('disconnected');
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleImageAnalysis = async () => {
    if (!selectedImage || loading) return;

    setLoading(true);
    addMessage('user', '📸 Analyzing uploaded image...');
    
    try {
      const formData = new FormData();
      formData.append('image', selectedImage);

      console.log('🚀 Sending image for analysis:', selectedImage.name);
      const response = await enhancedAIAPI.recognizeFood(formData);
      
      if (response?.data?.success) {
        const data = response.data.data;
        let analysisText = `🔍 **Food Analysis Results:**\n\n`;
        
        if (data.detected_foods && data.detected_foods.length > 0) {
          analysisText += `**Detected Items:**\n`;
          data.detected_foods.forEach((food: any) => {
            analysisText += `• ${food.name} (${Math.round(food.confidence * 100)}% confidence)\n`;
          });
        }

        if (data.recipe_suggestion) {
          const recipe = data.recipe_suggestion;
          analysisText += `\n🍳 **Recipe Suggestion: ${recipe.title}**\n`;
          analysisText += `${recipe.description}\n\n`;
          analysisText += `⏱️ Prep: ${recipe.prep_time}m | Cook: ${recipe.cook_time}m | Serves: ${recipe.servings}\n`;
          analysisText += `📊 Difficulty: ${recipe.difficulty}\n\n`;
          
          if (recipe.ingredients && recipe.ingredients.length > 0) {
            analysisText += `**Ingredients:**\n`;
            recipe.ingredients.forEach((ing: string) => {
              analysisText += `• ${ing}\n`;
            });
          }

          if (recipe.basic_steps && recipe.basic_steps.length > 0) {
            analysisText += `\n**Basic Steps:**\n`;
            recipe.basic_steps.forEach((step: string, idx: number) => {
              analysisText += `${idx + 1}. ${step}\n`;
            });
          }
        }

        if (data.cooking_tips && data.cooking_tips.length > 0) {
          analysisText += `\n💡 **Cooking Tips:**\n`;
          data.cooking_tips.forEach((tip: string) => {
            analysisText += `• ${tip}\n`;
          });
        }

        addMessage('ai', analysisText);
        console.log('✅ Image analysis successful');
      } else {
        addMessage('error', `Sorry, I couldn't analyze the image: ${response?.data?.message || 'Unknown error'}`);
        console.error('❌ Image analysis error:', response?.data?.message);
      }
    } catch (error: any) {
      console.error('❌ Image analysis error:', error);
      const errorMessage = error.message || 'Sorry, I had trouble analyzing the image. Please check the connection and try again.';
      addMessage('error', errorMessage);
    } finally {
      setLoading(false);
      setSelectedImage(null);
      setImagePreview(null);
    }
  };

  const handleRecipeGeneration = async () => {
    if (!ingredients.trim() || loading) return;

    setLoading(true);
    addMessage('user', `Generate a recipe using: ${ingredients}`);

    try {
      const requestData = {
        ingredients,
        ...preferences,
        time_constraint: preferences.time_constraint ? parseInt(preferences.time_constraint) : undefined
      };

      console.log('🚀 Generating recipe with data:', requestData);
      const response = await enhancedAIAPI.generateRecipe(requestData);
      
      if (response?.data?.success && response?.data?.data?.recipe) {
        const recipe = response.data.data.recipe;
        let recipeText = `🍳 **${recipe.title}**\n\n`;
        recipeText += `${recipe.description}\n\n`;
        recipeText += `⏱️ Prep: ${recipe.prep_time}m | Cook: ${recipe.cook_time}m | Serves: ${recipe.servings}\n`;
        recipeText += `📊 Difficulty: ${recipe.difficulty} | 🌍 Cuisine: ${recipe.cuisine}\n\n`;

        if (recipe.ingredients && recipe.ingredients.length > 0) {
          recipeText += `**Ingredients:**\n`;
          recipe.ingredients.forEach((ing: any) => {
            recipeText += `• ${ing.quantity} ${ing.unit} ${ing.name}${ing.notes ? ` (${ing.notes})` : ''}\n`;
          });
        }

        if (recipe.instructions && recipe.instructions.length > 0) {
          recipeText += `\n**Instructions:**\n`;
          recipe.instructions.forEach((inst: any) => {
            recipeText += `${inst.step_number}. ${inst.instruction}`;
            if (inst.time_minutes) recipeText += ` (${inst.time_minutes} minutes)`;
            if (inst.temperature) recipeText += ` at ${inst.temperature}`;
            recipeText += `\n`;
          });
        }

        if (recipe.nutrition) {
          const nutrition = recipe.nutrition;
          recipeText += `\n**Nutrition (per serving):**\n`;
          recipeText += `• Calories: ${nutrition.calories_per_serving || 'N/A'}\n`;
          recipeText += `• Protein: ${nutrition.protein_grams || 'N/A'}g | Carbs: ${nutrition.carbs_grams || 'N/A'}g | Fat: ${nutrition.fat_grams || 'N/A'}g\n`;
        }

        if (response?.data?.data?.notes) {
          recipeText += `\n💡 **Chef's Notes:**\n${response.data.data.notes}`;
        }

        addMessage('ai', recipeText);
        console.log('✅ Recipe generation successful');
      } else {
        addMessage('error', `Sorry, I couldn't generate a recipe: ${response?.data?.message || 'Unknown error'}`);
        console.error('❌ Recipe generation error:', response?.data?.message);
      }
    } catch (error: any) {
      console.error('❌ Recipe generation error:', error);
      const errorMessage = error.message || 'Sorry, I had trouble generating a recipe. Please check the connection and try again.';
      addMessage('error', errorMessage);
    } finally {
      setLoading(false);
      setIngredients('');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-50 p-4">
      {/* Connection Diagnostic Component */}
      <ConnectionDiagnostic />
      
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">OnlyPans AI Assistant</h1>
                <p className="text-gray-600">Your intelligent cooking companion powered by Gemini AI</p>
              </div>
            </div>
            
            {/* Connection Status */}
            <div className="flex items-center space-x-2">
              {useMockAPI ? (
                <div className="flex items-center space-x-2 px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">
                  <WifiOff className="w-4 h-4" />
                  <span>Demo Mode</span>
                  <button 
                    onClick={() => {setUseMockAPI(false); setConnectionStatus('checking');}}
                    className="ml-2 text-xs underline hover:no-underline"
                  >
                    Try Real API
                  </button>
                </div>
              ) : connectionStatus === 'connected' ? (
                <div className="flex items-center space-x-2 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                  <Wifi className="w-4 h-4" />
                  <span>Connected</span>
                </div>
              ) : connectionStatus === 'disconnected' ? (
                <div className="flex items-center space-x-2 px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm">
                  <WifiOff className="w-4 h-4" />
                  <span>Disconnected</span>
                  <button 
                    onClick={() => setUseMockAPI(true)}
                    className="ml-2 text-xs underline hover:no-underline"
                  >
                    Use Demo
                  </button>
                </div>
              ) : (
                <div className="flex items-center space-x-2 px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm">
                  <div className="w-4 h-4 border-2 border-gray-300 border-t-gray-600 rounded-full animate-spin"></div>
                  <span>Checking...</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-2xl shadow-lg mb-6">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex-1 flex items-center justify-center space-x-2 py-4 px-6 font-medium transition-colors ${
                activeTab === 'chat'
                  ? 'text-orange-600 border-b-2 border-orange-600 bg-orange-50'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <MessageCircle className="w-5 h-5" />
              <span>AI Chat</span>
            </button>
            <button
              onClick={() => setActiveTab('image')}
              className={`flex-1 flex items-center justify-center space-x-2 py-4 px-6 font-medium transition-colors ${
                activeTab === 'image'
                  ? 'text-orange-600 border-b-2 border-orange-600 bg-orange-50'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <Camera className="w-5 h-5" />
              <span>Image to Recipe</span>
            </button>
            <button
              onClick={() => setActiveTab('recipe')}
              className={`flex-1 flex items-center justify-center space-x-2 py-4 px-6 font-medium transition-colors ${
                activeTab === 'recipe'
                  ? 'text-orange-600 border-b-2 border-orange-600 bg-orange-50'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <ChefHat className="w-5 h-5" />
              <span>Recipe Generator</span>
            </button>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'chat' && (
              <div className="space-y-6">
                {/* Chat Messages */}
                <div className="h-96 overflow-y-auto space-y-4 p-4 bg-gray-50 rounded-xl">
                  {chatMessages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg whitespace-pre-wrap ${
                          message.type === 'user'
                            ? 'bg-orange-500 text-white'
                            : message.type === 'error'
                            ? 'bg-red-50 text-red-800 shadow-sm border border-red-200'
                            : 'bg-white text-gray-800 shadow-sm border'
                        }`}
                      >
                        {message.type === 'error' && (
                          <div className="flex items-center space-x-2 mb-2">
                            <AlertCircle className="w-4 h-4 text-red-500" />
                            <span className="text-sm font-medium text-red-600">Connection Error</span>
                          </div>
                        )}
                        {message.content}
                      </div>
                    </div>
                  ))}
                  {loading && (
                    <div className="flex justify-start">
                      <div className="bg-white text-gray-800 shadow-sm border px-4 py-2 rounded-lg">
                        <div className="flex items-center space-x-2">
                          <div className="animate-spin rounded-full h-4 w-4 border-2 border-orange-200 border-t-orange-600"></div>
                          <span>AI is thinking...</span>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={chatEndRef} />
                </div>

                {/* Chat Input */}
                <div className="flex space-x-4">
                  <input
                    type="text"
                    value={currentMessage}
                    onChange={(e) => setCurrentMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Ask me anything about cooking, recipes, or nutrition..."
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    disabled={loading}
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={loading || !currentMessage.trim()}
                    className="px-6 py-3 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-xl hover:from-orange-600 hover:to-red-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
              </div>
            )}

            {activeTab === 'image' && (
              <div className="space-y-6">
                <div className="text-center">
                  <Camera className="w-16 h-16 text-orange-500 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Upload Food Image</h3>
                  <p className="text-gray-600 mb-6">
                    Upload a photo of food or ingredients and I'll analyze it and suggest a recipe!
                  </p>
                </div>

                {/* Image Upload Area */}
                <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-orange-500 transition-colors">
                  {imagePreview ? (
                    <div className="space-y-4">
                      <div className="relative inline-block">
                        <img
                          src={imagePreview}
                          alt="Food preview"
                          className="max-w-xs max-h-64 rounded-lg shadow-lg"
                        />
                        <button
                          onClick={() => {
                            setSelectedImage(null);
                            setImagePreview(null);
                          }}
                          className="absolute -top-2 -right-2 w-8 h-8 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-colors"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                      <button
                        onClick={handleImageAnalysis}
                        disabled={loading}
                        className="px-6 py-3 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-xl hover:from-orange-600 hover:to-red-600 transition-all duration-300 disabled:opacity-50"
                      >
                        {loading ? (
                          <div className="flex items-center space-x-2">
                            <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                            <span>Analyzing...</span>
                          </div>
                        ) : (
                          <>
                            <Sparkles className="w-5 h-5 inline mr-2" />
                            Analyze & Get Recipe
                          </>
                        )}
                      </button>
                    </div>
                  ) : (
                    <div>
                      <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-600 mb-4">
                        Drag and drop an image here, or click to select
                      </p>
                      <button
                        onClick={() => fileInputRef.current?.click()}
                        className="px-6 py-3 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-xl hover:from-orange-600 hover:to-red-600 transition-all duration-300"
                      >
                        Choose Image
                      </button>
                      <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/*"
                        onChange={handleImageUpload}
                        className="hidden"
                      />
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'recipe' && (
              <div className="space-y-6">
                <div className="text-center">
                  <ChefHat className="w-16 h-16 text-orange-500 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Recipe Generator</h3>
                  <p className="text-gray-600 mb-6">
                    Tell me what ingredients you have and I'll create a custom recipe for you!
                  </p>
                </div>

                {/* Ingredients Input */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Available Ingredients
                  </label>
                  <textarea
                    value={ingredients}
                    onChange={(e) => setIngredients(e.target.value)}
                    placeholder="Enter your ingredients (e.g., chicken breast, bell peppers, onions, garlic, rice...)"
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    rows={3}
                  />
                </div>

                {/* Preferences */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Dietary Restrictions
                    </label>
                    <input
                      type="text"
                      value={preferences.dietary_restrictions}
                      onChange={(e) => setPreferences(prev => ({ ...prev, dietary_restrictions: e.target.value }))}
                      placeholder="e.g., vegetarian, gluten-free, dairy-free"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Cuisine Preference
                    </label>
                    <input
                      type="text"
                      value={preferences.cuisine_preference}
                      onChange={(e) => setPreferences(prev => ({ ...prev, cuisine_preference: e.target.value }))}
                      placeholder="e.g., Italian, Asian, Mexican"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Difficulty Level
                    </label>
                    <select
                      value={preferences.difficulty_preference}
                      onChange={(e) => setPreferences(prev => ({ ...prev, difficulty_preference: e.target.value }))}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    >
                      <option value="easy">Easy</option>
                      <option value="medium">Medium</option>
                      <option value="hard">Hard</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Servings
                    </label>
                    <input
                      type="number"
                      min="1"
                      max="12"
                      value={preferences.servings}
                      onChange={(e) => setPreferences(prev => ({ ...prev, servings: parseInt(e.target.value) || 4 }))}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    />
                  </div>
                </div>

                {/* Generate Button */}
                <button
                  onClick={handleRecipeGeneration}
                  disabled={loading || !ingredients.trim()}
                  className="w-full px-6 py-4 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-xl hover:from-orange-600 hover:to-red-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                >
                  {loading ? (
                    <div className="flex items-center justify-center space-x-2">
                      <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                      <span>Generating Recipe...</span>
                    </div>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5 inline mr-2" />
                      Generate Custom Recipe
                    </>
                  )}
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Tips */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">💡 Tips for Better Results</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
            <div>
              <strong>Chat:</strong> Ask specific questions about cooking techniques, ingredient substitutions, or nutritional information.
            </div>
            <div>
              <strong>Image Analysis:</strong> Use clear, well-lit photos with food as the main focus for best recognition.
            </div>
            <div>
              <strong>Recipe Generation:</strong> List specific ingredients and mention any preferences for more tailored recipes.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
