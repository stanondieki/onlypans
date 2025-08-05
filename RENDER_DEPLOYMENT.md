# 🚀 OnlyPans Render Deployment Guide

Simple deployment guide for OnlyPans on Render.

## 📋 Quick Setup

### 1. Create PostgreSQL Database
1. **Render Dashboard** → **New +** → **PostgreSQL**
2. **Name**: `onlypans-db`
3. **Copy Internal Database URL**

### 2. Create Web Service
1. **New +** → **Web Service**
2. **Connect Repository**: `stanondieki/onlypans`
3. **Configuration**:
   - **Root Directory**: Leave blank
   - **Build Command**: `cd backend && pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
   - **Start Command**: `cd backend && gunicorn onlypans_backend.wsgi:application --bind 0.0.0.0:$PORT`

### 3. Environment Variables
```env
SECRET_KEY=9o9%x)atmzg=iww3$x=aka3hod&i)(pf$%l2l)2igy8ts3zi(i
DEBUG=False
DJANGO_SETTINGS_MODULE=onlypans_backend.production_settings
CORS_ALLOWED_ORIGINS=https://onlypans-ctfazewa7-stanondiekis-projects.vercel.app
DATABASE_URL=your-postgres-internal-url-here
PYTHON_VERSION=3.12.0
```

### 4. Optional: AI Features
```env
GOOGLE_API_KEY=your-google-gemini-api-key
```

### 5. Deploy
Click **"Create Web Service"** and wait for deployment.

### 6. Test
- Health: `https://your-app.onrender.com/api/health/`
- Admin: `https://your-app.onrender.com/admin/`

## 🔧 Update Frontend
Update Vercel environment variable:
```env
NEXT_PUBLIC_API_URL=https://your-app.onrender.com/api
```

---
**That's it! Your OnlyPans app should be live.** 🎉
