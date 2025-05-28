web: gunicorn library_system.wsgi --log-file=- -w 3 --timeout 25
release: python manage.py collectstatic --noinput && python manage.py migrate