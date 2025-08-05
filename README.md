# OnlyPans - Intelligent Meal Planning Assistant

OnlyPans is a comprehensive meal planning and recipe assistant application that replaces manual handwritten meal timetables with smart, AI-powered digital meal planning. Built with Next.js TypeScript frontend and Django backend, it features AI-powered recipe suggestions using Google Gemini, image recognition for food identification, and step-by-step cooking instructions.

## 🚀 Features

### Core Features
- **Digital Meal Planning**: Interactive weekly meal plans with drag-and-drop functionality
- **Recipe Management**: Create, edit, and discover recipes with detailed instructions and nutritional information
- **AI-Powered Recipe Generation**: Generate recipes from ingredients using Google Gemini AI
- **Food Image Recognition**: Upload photos to identify dishes and get recipe suggestions
- **Smart Shopping Lists**: Auto-generate shopping lists from meal plans
- **User Profiles**: Customizable profiles with dietary preferences and cooking skill levels

### AI Integration
- **Google Gemini AI**: Advanced recipe generation and food recognition
- **Ingredient Suggestions**: Get complementary ingredient recommendations
- **Meal Planning Assistance**: AI-powered meal planning suggestions
- **Image Analysis**: Identify food items and dishes from photos

### Technical Features
- **Authentication & Authorization**: JWT-based secure user authentication
- **RESTful API**: Comprehensive Django REST Framework API
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Real-time Updates**: Dynamic UI updates with Zustand state management
- **File Upload**: Support for recipe and food images

## 🛠 Technology Stack

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **Axios**: HTTP client for API requests
- **Lucide React**: Beautiful icons
- **React Dropzone**: File upload handling
- **Date-fns**: Date manipulation

### Backend
- **Django 5.2.3**: Python web framework
- **Django REST Framework**: API development
- **PostgreSQL/SQLite**: Database (configurable)
- **Google Generative AI**: AI integration
- **JWT Authentication**: Secure token-based auth
- **Redis**: Caching (optional)
- **Pillow**: Image processing

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm
- Python 3.12+
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd OnlyPans/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\\Scripts\\Activate.ps1  # Windows PowerShell
   # or
   source venv/bin/activate     # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python create_superuser.py
   ```

7. **Create sample data**
   ```bash
   python create_sample_data.py
   ```

8. **Start the server**
   ```bash
   python manage.py runserver 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (PostgreSQL)
DB_NAME=onlypans_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Use SQLite for development (set to False to use PostgreSQL)
USE_SQLITE=True

# Redis Configuration
REDIS_URL=redis://127.0.0.1:6379/1

# Google Gemini AI API Key
GOOGLE_API_KEY=your-google-api-key-here
```

### Google Gemini AI Setup

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add the key to your `.env` file as `GOOGLE_API_KEY`
3. The AI features will be automatically enabled

## 📁 Project Structure

```
OnlyPans/
├── backend/
│   ├── accounts/           # User authentication and profiles
│   ├── recipes/            # Recipe management
│   ├── meals/              # Meal planning and shopping lists
│   ├── ai_assistant/       # AI integration and services
│   ├── onlypans_backend/   # Django project settings
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── app/            # Next.js app router pages
│   │   ├── components/     # Reusable React components
│   │   ├── lib/            # Utility functions and API client
│   │   ├── store/          # Zustand state management
│   │   └── types/          # TypeScript type definitions
│   ├── public/             # Static assets
│   ├── package.json
│   └── next.config.ts
└── README.md
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Recipes
- `GET /api/recipes/` - List recipes (with filtering and search)
- `POST /api/recipes/` - Create new recipe
- `GET /api/recipes/{id}/` - Get recipe details
- `PUT /api/recipes/{id}/` - Update recipe
- `DELETE /api/recipes/{id}/` - Delete recipe
- `POST /api/recipes/{id}/rate/` - Rate a recipe
- `POST /api/recipes/{id}/favorite/` - Toggle favorite status

### Meal Planning
- `GET /api/meals/plans/` - List meal plans
- `POST /api/meals/plans/` - Create meal plan
- `GET /api/meals/plans/{id}/` - Get meal plan details
- `GET /api/meals/plans/{id}/shopping-list/` - Get shopping list
- `POST /api/meals/plans/{id}/generate-shopping-list/` - Generate shopping list

### AI Assistant
- `POST /api/ai/recognize-food/` - Recognize food from image
- `POST /api/ai/generate-recipe/` - Generate recipe from ingredients
- `POST /api/ai/suggest-ingredients/` - Get ingredient suggestions
- `GET /api/ai/status/` - Check AI service status

## 🎯 Usage

### Getting Started
1. **Access the application**: Open http://localhost:3000
2. **Create an account**: Register a new user account
3. **Explore recipes**: Browse the recipe collection
4. **Create meal plans**: Plan your weekly meals
5. **Try AI features**: Upload food images or generate recipes

### Key Features Usage

#### Meal Planning
1. Navigate to the Meals page
2. Create a new meal plan with start/end dates
3. Add recipes to specific days and meal types
4. Generate shopping lists automatically

#### AI Recipe Generation
1. Go to the AI Assistant page
2. Enter available ingredients
3. Specify dietary preferences (optional)
4. Generate custom recipes with AI

#### Food Recognition
1. Upload a food image in the AI Assistant
2. Get identified food items and confidence scores
3. Receive recipe suggestions based on the image

## 🧪 Testing

### Backend Testing
```bash
cd backend
python test_api.py
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Backend Deployment
1. Set `DEBUG=False` in production
2. Configure PostgreSQL database
3. Set up Redis for caching
4. Use production WSGI server (Gunicorn)
5. Configure static files serving

### Frontend Deployment
```bash
npm run build
npm start
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please create an issue in the GitHub repository or contact the development team.

## 🙏 Acknowledgments

- Google Gemini AI for powerful recipe generation
- Next.js team for the excellent React framework
- Django REST Framework for robust API development
- Tailwind CSS for beautiful styling
- All open-source contributors

---

**OnlyPans** - Transform your meal planning with AI-powered assistance! 🍳✨
