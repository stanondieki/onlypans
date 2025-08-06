# 🤖 Setting Up Gemini AI API Key

## Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

## Step 2: Add API Key to Render Environment

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Find your "onlypans" service
3. Click on it → Go to "Environment" tab
4. Click "Add Environment Variable"
5. Add:
   - **Key**: `GOOGLE_AI_API_KEY`
   - **Value**: `your-actual-api-key-here`
6. Click "Save Changes"

## Step 3: Redeploy (if needed)

The service should automatically redeploy when you add the environment variable. If not:
1. Go to "Manual Deploy" tab
2. Click "Deploy Latest Commit"

## Step 4: Test AI Features

Once deployed with the API key:

### Backend Test:
Visit: `https://onlypans.onrender.com/api/ai/status/`
Should return: `{"available": true, "message": "AI service is available"}`

### Frontend Test:
1. Go to: https://onlypans-ctfazewa7-stanondiekis-projects.vercel.app/ai
2. Try the chat feature
3. Upload an image for recipe suggestions
4. Generate recipes from ingredients

## Features Available:

### 🗨️ AI Chat
- Ask any cooking or food-related questions
- Get cooking tips, techniques, and advice
- Ask about nutrition, substitutions, meal planning

### 📸 Image to Recipe
- Upload photos of food or ingredients
- Get detailed food analysis
- Receive recipe suggestions based on what's detected
- Automatic recipe creation for high-confidence matches

### 🍳 Recipe Generator
- Input available ingredients
- Set dietary restrictions and preferences
- Specify cuisine, difficulty, and serving size
- Get complete recipes with ingredients and instructions

## Example Questions for AI Chat:

- "How do I properly season a cast iron pan?"
- "What's a good substitute for eggs in baking?"
- "How long should I marinate chicken for?"
- "What spices go well with lamb?"
- "How do I know when pasta is perfectly al dente?"

## Troubleshooting:

### AI Service Not Available
- Check that the API key is correctly set in Render environment
- Ensure the key hasn't expired (Google AI keys don't expire by default)
- Check the service logs in Render for any error messages

### Slow Responses
- First request may be slower due to Render cold start
- Gemini API responses typically take 2-5 seconds

### Poor Image Recognition
- Use clear, well-lit photos
- Make sure food is the main subject
- Try different angles or lighting

## Rate Limits:

Google AI Studio free tier includes:
- 15 requests per minute
- 1,500 requests per day

For production use, consider upgrading to a paid plan.
