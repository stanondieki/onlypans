# OnlyPans - Local Development

A meal planning application built with Django REST API backend and Next.js frontend.

## Prerequisites

- Python 3.12+
- Node.js 18+
- npm or yarn

## Quick Start

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Start Django development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start Next.js development server:
   ```bash
   npm run dev
   ```

## Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Django Admin: http://localhost:8000/admin

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and configure:
- `GOOGLE_API_KEY`: For AI-powered recipe suggestions (optional)

## Project Structure

```
OnlyPans/
├── backend/          # Django REST API
│   ├── accounts/     # User authentication
│   ├── meals/        # Meal planning
│   ├── recipes/      # Recipe management
│   └── ai_assistant/ # AI features
├── frontend/         # Next.js application
└── README.md
```

## Development Notes

- Uses SQLite database for local development
- CORS configured for localhost:3000
- Debug mode enabled for development
- Simple console logging