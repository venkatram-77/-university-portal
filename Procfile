web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn university_portal.wsgi:application --bind 0.0.0.0:$PORT
