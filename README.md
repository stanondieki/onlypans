# OnlyPans - Local Development Setup

This guide will help you set up the OnlyPans application for local development.

## Prerequisites

- **Python 3.8+** (for Django backend)
- **Node.js 18+** (for Next.js frontend)
- **Git** (for version control)

## Quick Setup

### Windows Users
```bash
setup-dev.bat
```

### macOS/Linux Users
```bash
chmod +x setup-dev.sh
./setup-dev.sh
```

## Manual Setup

### Backend Setup (Django)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Update the values as needed (especially `GOOGLE_API_KEY` if using AI features)

6. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup (Next.js)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

## Development URLs

- **Frontend Application:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Django Admin Panel:** http://localhost:8000/admin
- **API Documentation:** http://localhost:8000/api/ (if configured)

## Project Structure

```
OnlyPans/
├── backend/                 # Django backend
│   ├── accounts/           # User authentication app
│   ├── ai_assistant/       # AI features app
│   ├── meals/              # Meals management app
│   ├── recipes/            # Recipes management app
│   ├── onlypans_backend/   # Main Django project
│   ├── manage.py           # Django management script
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── frontend/               # Next.js frontend
│   ├── src/               # Source code
│   ├── public/            # Static assets
│   ├── package.json       # Node.js dependencies
│   └── .env.local         # Environment variables
└── README.md              # This file
```

## Environment Variables

### Backend (.env)
- `SECRET_KEY`: Django secret key
- `DEBUG`: Enable debug mode (True for development)
- `USE_SQLITE`: Use SQLite database (True for development)
- `GOOGLE_API_KEY`: Google AI API key (for AI features)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_API_BASE_URL`: Backend base URL

## Database

By default, the project uses SQLite for development (no setup required). 

To use PostgreSQL:
1. Install PostgreSQL
2. Create a database named `onlypans_db`
3. Update `.env` file with database credentials
4. Set `USE_SQLITE=False` in `.env`

## AI Features

To use AI features:
1. Get a Google AI API key from Google AI Studio
2. Add it to `GOOGLE_API_KEY` in the backend `.env` file

## Common Commands

### Backend
```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

### Frontend
```bash
# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

## Troubleshooting

1. **Port already in use:** Change the port by running `python manage.py runserver 8001` for backend or modify the Next.js config for frontend.

2. **Module not found:** Make sure you've activated the virtual environment and installed all dependencies.

3. **Database errors:** Run `python manage.py migrate` to apply database migrations.

4. **CORS errors:** Make sure the frontend URL is in `CORS_ALLOWED_ORIGINS` in Django settings.

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## Support

If you encounter any issues, please check the troubleshooting section or create an issue in the repository.
