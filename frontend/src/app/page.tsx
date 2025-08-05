import Link from 'next/link';
import { ChefHat, Clock, Sparkles, ArrowRight, Star, Users, Zap, Brain } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-pink-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Background decoration */}
        <div className="absolute inset-0 bg-gradient-to-r from-orange-600/10 to-red-600/10 transform -skew-y-2 origin-top-left"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-32">
          <div className="text-center">
            {/* Logo and Title with animation */}
            <div className="flex justify-center mb-8 animate-pulse">
              <div className="flex items-center space-x-3 bg-white/80 backdrop-blur-sm rounded-2xl px-6 py-4 shadow-lg">
                <div className="relative">
                  <ChefHat className="w-16 h-16 text-orange-600" />
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full animate-bounce"></div>
                </div>
                <h1 className="text-7xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
                  OnlyPans
                </h1>
              </div>
            </div>
            
            <p className="text-2xl text-gray-700 mb-4 max-w-4xl mx-auto font-light">
              Transform your kitchen experience with 
              <span className="font-semibold text-orange-600"> AI-powered </span>
              meal planning
            </p>
            
            <p className="text-lg text-gray-600 mb-12 max-w-3xl mx-auto">
              Say goodbye to handwritten meal timetables. Welcome to intelligent recipe discovery, 
              smart meal scheduling, and effortless cooking automation.
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
              <Link
                href="/meals"
                className="group bg-gradient-to-r from-orange-600 to-red-600 text-white px-10 py-4 rounded-2xl font-semibold hover:from-orange-700 hover:to-red-700 transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-2xl flex items-center gap-3"
              >
                Start Planning Meals
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/upload"
                className="group border-2 border-orange-600 text-orange-600 px-10 py-4 rounded-2xl font-semibold hover:bg-orange-600 hover:text-white transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center gap-3"
              >
                <Sparkles className="w-5 h-5" />
                Try AI Assistant
              </Link>
            </div>
            
            {/* Stats */}
            <div className="mt-16 grid grid-cols-3 gap-8 max-w-2xl mx-auto">
              <div className="text-center">
                <div className="text-3xl font-bold text-orange-600">1000+</div>
                <div className="text-sm text-gray-600">Recipes Generated</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-orange-600">500+</div>
                <div className="text-sm text-gray-600">Happy Families</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-orange-600">95%</div>
                <div className="text-sm text-gray-600">Success Rate</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Everything You Need for 
            <span className="text-orange-600"> Smart Cooking</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            From AI-powered recipe generation to intelligent meal planning, 
            OnlyPans makes cooking enjoyable and effortless.
          </p>
        </div>
        
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="group bg-white p-8 rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
            <div className="bg-gradient-to-br from-orange-100 to-red-100 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
              <Clock className="h-8 w-8 text-orange-600" />
            </div>
            <h3 className="text-2xl font-bold mb-4 text-gray-900 text-center">Smart Scheduling</h3>
            <p className="text-gray-600 text-center leading-relaxed">
              Create weekly meal plans with intuitive drag-and-drop. 
              Schedule breakfast, lunch, and dinner with automatic shopping list generation.
            </p>
            <div className="mt-6 flex justify-center">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-orange-100 text-orange-800">
                <Star className="w-4 h-4 mr-1" />
                Most Popular
              </span>
            </div>
          </div>
          
          {/* Feature 2 */}
          <div className="group bg-white p-8 rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
            <div className="bg-gradient-to-br from-blue-100 to-purple-100 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
              <Sparkles className="h-8 w-8 text-blue-600" />
            </div>
            <h3 className="text-2xl font-bold mb-4 text-gray-900 text-center">AI-Powered Magic</h3>
            <p className="text-gray-600 text-center leading-relaxed">
              Upload ingredient photos or describe what you have. 
              Get personalized recipe recommendations powered by advanced AI.
            </p>
            <div className="mt-6 flex justify-center">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                <Zap className="w-4 h-4 mr-1" />
                AI Powered
              </span>
            </div>
          </div>
          
          {/* Feature 3 */}
          <div className="group bg-white p-8 rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
            <div className="bg-gradient-to-br from-green-100 to-teal-100 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
              <ChefHat className="h-8 w-8 text-green-600" />
            </div>
            <h3 className="text-2xl font-bold mb-4 text-gray-900 text-center">Step-by-Step Guidance</h3>
            <p className="text-gray-600 text-center leading-relaxed">
              Follow detailed cooking instructions with built-in timers, tips, 
              and nutritional information for every recipe.
            </p>
            <div className="mt-6 flex justify-center">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                <Users className="w-4 h-4 mr-1" />
                Beginner Friendly
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Features Section */}
      <div className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Powered by Advanced <span className="text-orange-600">AI Technology</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Experience the future of cooking with cutting-edge artificial intelligence 
              that understands your preferences and helps you cook better.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="text-center p-6 bg-white rounded-lg shadow-md">
              <Brain className="w-12 h-12 text-orange-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-3">AI Recipe Recognition</h3>
              <p className="text-gray-600">
                Upload a photo of any dish and get instant recipe suggestions with 
                step-by-step cooking instructions powered by AI.
              </p>
            </div>
            
            <div className="text-center p-6 bg-white rounded-lg shadow-md">
              <Sparkles className="w-12 h-12 text-orange-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-3">Smart Suggestions</h3>
              <p className="text-gray-600">
                Get personalized meal recommendations based on your preferences, 
                dietary needs, and available ingredients.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-orange-600 to-red-600 text-white py-16">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-4">Ready to Revolutionize Your Meal Planning?</h2>
          <p className="text-xl mb-8 text-orange-100">
            Join thousands of families who have upgraded from manual meal planning to smart, AI-powered solutions.
          </p>
          <Link
            href="/meals"
            className="bg-white text-orange-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors inline-flex items-center gap-2"
          >
            Get Started Today
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
