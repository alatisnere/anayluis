web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py seed_demo && gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 2
