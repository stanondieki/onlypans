web: cd backend && gunicorn onlypans_backend.wsgi:application --bind 0.0.0.0:$PORT
release: cd backend && python manage.py migrate && python manage.py collectstatic --no-input
