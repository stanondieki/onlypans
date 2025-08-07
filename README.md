# OnlyPans - AI-Powered Meal Planning App

A modern meal planning application with AI assistance, built with Django (backend) and Next.js (frontend).

## 🚀 Quick Deployment

### Backend (Render)
1. Connect your GitHub repo to Render
2. Set these environment variables in Render:
   - `GOOGLE_AI_API_KEY`: Your Google AI API key
   - `SECRET_KEY`: Django secret key
   - `DEBUG`: False

### Frontend (Vercel)
1. Connect your GitHub repo to Vercel
2. Set the environment variable:
   - `NEXT_PUBLIC_API_URL`: https://onlypans-backend.onrender.com

## 🛠️ Local Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your values
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure
```
OnlyPans/
├── backend/           # Django API
│   ├── accounts/      # User authentication
│   ├── ai_assistant/  # AI features
│   ├── meals/         # Meal management
│   └── recipes/       # Recipe management
├── frontend/          # Next.js app
└── render.yaml        # Render deployment config
```

## 🔗 Live URLs
- **Backend**: https://onlypans-backend.onrender.com
- **Frontend**: Will be provided after Vercel deployment
